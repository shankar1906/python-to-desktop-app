use std::env;
use std::net::TcpStream;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::thread;
use std::time::Duration;
use tauri::Manager;

fn find_project_dir(search_roots: &[PathBuf]) -> Option<PathBuf> {
  for root in search_roots {
    let mut current = root.clone();
    loop {
      if current.join("start_backend.py").exists() && current.join("manage.py").exists() {
        return Some(current);
      }

      if !current.pop() {
        break;
      }
    }
  }

  None
}

fn find_python_executable(project_dir: &Path) -> Option<String> {
  let windows_candidates = [
    project_dir.join("venv").join("Scripts").join("python.exe"),
    project_dir.join("venv").join("Scripts").join("python"),
  ];

  let unix_candidates = [
    project_dir.join("venv").join("bin").join("python"),
    project_dir.join("venv").join("bin").join("python3"),
  ];

  let candidates = if cfg!(windows) {
    &windows_candidates[..]
  } else {
    &unix_candidates[..]
  };

  for candidate in candidates {
    if candidate.exists() {
      return candidate.to_str().map(|value| value.to_string());
    }
  }

  if cfg!(windows) {
    Some("python".to_string())
  } else {
    Some("python3".to_string())
  }
}

fn wait_for_backend(host: &str, port: u16, timeout_secs: u64) -> bool {
  let deadline = std::time::Instant::now() + Duration::from_secs(timeout_secs);
  while std::time::Instant::now() < deadline {
    if TcpStream::connect(format!("{host}:{port}"))
      .map(|_| true)
      .unwrap_or(false)
    {
      return true;
    }
    thread::sleep(Duration::from_secs(1));
  }

  false
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .setup(|app| {
      if cfg!(debug_assertions) {
        app.handle().plugin(
          tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build(),
        )?;
      }

      let app_dir = app
        .path()
        .resource_dir()
        .unwrap_or_else(|_| app.path().app_local_data_dir().unwrap());

      let current_dir = env::current_dir().unwrap_or_else(|_| PathBuf::from("."));
      let search_roots = [
        app_dir.clone(),
        current_dir.clone(),
        app_dir.join(r"..\..\.."),
        app_dir.join(r"..\..\..\.."),
      ];

      if let Some(project_dir) = find_project_dir(&search_roots) {
        let backend_script = project_dir.join("start_backend.py");
        let python_executable = find_python_executable(&project_dir);

        if backend_script.exists() {
          let project_dir_clone = project_dir.clone();
          let python_executable_clone = python_executable.clone();
          thread::spawn(move || {
            if let Some(python) = python_executable_clone {
              let mut command = Command::new(&python);
              command
                .arg(&backend_script)
                .current_dir(&project_dir_clone)
                .stdout(Stdio::null())
                .stderr(Stdio::null());

              #[cfg(windows)]
              {
                use std::os::windows::process::CommandExt;
                const CREATE_NO_WINDOW: u32 = 0x0800_0000;
                command.creation_flags(CREATE_NO_WINDOW);
              }

              let _ = command.spawn();
            }
          });

          if wait_for_backend("127.0.0.1", 8000, 30) {
            println!("Backend is ready at http://127.0.0.1:8000");
          } else {
            eprintln!("Backend did not become ready on time");
          }
        }
      } else {
        eprintln!("Unable to locate the project root for the backend process");
      }

      Ok(())
    })
    .build(tauri::generate_context!())
    .expect("error while running tauri application")
    .run(|_app_handle, _event| {});
}