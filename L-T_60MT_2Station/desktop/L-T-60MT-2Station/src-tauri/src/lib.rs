use std::process::Command;
use std::os::windows::process::CommandExt;
use tauri::Manager;

// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            // Find the bundled resources directory
            let resource_path = app.path().resource_dir().expect("failed to get resource dir");
            
            let mut root_path = if cfg!(debug_assertions) {
                // Dev mode: Go up from src-tauri/
                resource_path.parent().and_then(|p| p.parent()).unwrap_or(&resource_path).to_path_buf()
            } else {
                // Production mode: Use resource_dir directly
                resource_path.clone()
            };

            // If we are in production, Tauri packages parent resources in _up_/_up_/_up_
            // We check if these folders exist and append them to the path
            for _ in 0..10 {
                let up_path = root_path.join("_up_");
                if up_path.exists() {
                    root_path = up_path;
                } else {
                    break;
                }
            }

            let waitress_path = root_path.join("venv").join("Scripts").join("waitress-serve.exe");

            
            const CREATE_NO_WINDOW: u32 = 0x08000000;
            
            match Command::new(&waitress_path)
                .args(&["--host=127.0.0.1", "--port=8000", "standard_soft.wsgi:application"])
                .current_dir(&root_path)
                .creation_flags(CREATE_NO_WINDOW)
                .spawn() {
                    Ok(_) => {
                        println!("Backend started successfully");
                        
                        // Wait for the backend to be ready on port 8000
                        let mut port_ready = false;
                        for _ in 0..100 { // Wait up to 20 seconds
                            if std::net::TcpStream::connect("127.0.0.1:8000").is_ok() {
                                port_ready = true;
                                break;
                            }
                            std::thread::sleep(std::time::Duration::from_millis(200));
                        }

                        if !port_ready {
                             let error_msg = "The Django backend started but failed to respond on port 8000 within 20 seconds.";
                             show_error_and_exit(error_msg);
                        } else {
                            // Backend is ready, navigate the window to the local Django server
                            let main_window = app.get_webview_window("main").expect("failed to get main window");
                            let _ = main_window.navigate("http://127.0.0.1:8000".parse().expect("failed to parse URL"));
                        }

                    },
                    Err(e) => {
                        let error_msg = format!(
                            "Failed to start Django backend.\nPath: {}\nError: {}\n\nPlease ensure the 'venv' and 'standard_soft' folders are present.",
                            waitress_path.display(),
                            e
                        );
                        show_error_and_exit(&error_msg);
                    }
                }

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

fn show_error_and_exit(error_msg: &str) {
    use std::ffi::OsStr;
    use std::os::windows::ffi::OsStrExt;
    use windows_sys::Win32::UI::WindowsAndMessaging::{MessageBoxW, MB_ICONERROR, MB_OK};

    let title: Vec<u16> = OsStr::new("Backend Error").encode_wide().chain(Some(0)).collect();
    let msg: Vec<u16> = OsStr::new(error_msg).encode_wide().chain(Some(0)).collect();

    unsafe {
        MessageBoxW(std::ptr::null_mut(), msg.as_ptr(), title.as_ptr(), MB_OK | MB_ICONERROR);
    }
    std::process::exit(1);
}




