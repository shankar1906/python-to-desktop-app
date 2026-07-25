# Self-Signing Instructions for Internal Use

This document explains how to self-sign the application and how to trust it on other Windows machines.

> Note: Self-signed certificates are only suitable for internal use on machines you control. They are not trusted by SmartScreen or external users by default.

## 1. Create a self-signed code signing certificate on your PC

Run PowerShell as Administrator and execute:

```powershell
$cert = New-SelfSignedCertificate `
  -Subject "CN=LT60MT-2Station Self-Signed" `
  -Type CodeSigningCert `
  -CertStoreLocation "Cert:\CurrentUser\My" `
  -KeyExportPolicy Exportable `
  -NotAfter (Get-Date).AddYears(2)

$pwd = ConvertTo-SecureString "YourPfxPassword" -AsPlainText -Force
Export-PfxCertificate `
  -Cert "Cert:\CurrentUser\My\$($cert.Thumbprint)" `
  -FilePath "C:\temp\lt60mt-2station.pfx" `
  -Password $pwd
```

- Replace `YourPfxPassword` with a strong password.
- This creates a `.pfx` file at `C:\temp\lt60mt-2station.pfx`.

## 2. Sign the app files on your PC

Use the signing tool from the Windows SDK. Update the path if your SDK version folder is different.

```powershell
$signtool = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.28000.0\x64\signtool.exe"
$cert = "C:\temp\lt60mt-2station.pfx"
$pass = "YourPfxPassword"
$tstamp = "http://timestamp.digicert.com"

& $signtool sign /f $cert /p $pass /fd SHA256 /tr $tstamp /td SHA256 `
  "D:\L-T_60MT_2Station\desktop\L-T_60MT_2STATION\src-tauri\target\release\l-t-60mt-2station.exe"

& $signtool sign /f $cert /p $pass /fd SHA256 /tr $tstamp /td SHA256 `
  "D:\L-T_60MT_2Station\desktop\L-T_60MT_2STATION\src-tauri\target\release\bundle\msi\l-t-60mt-2station_0.1.0_x64_en-US.msi"
```

## 3. Confirm signing succeeded

1. Right-click the signed file (`.exe` or `.msi`).
2. Choose `Properties`.
3. Go to the `Digital Signatures` tab.
4. Confirm your certificate is listed.

## 4. Export the public certificate for other PCs

If you want the other machines to trust the signed app, export the certificate public key.

### Export public certificate

1. Open `certmgr.msc`.
2. Find the certificate under `Personal` -> `Certificates`.
3. Right-click the certificate, select `All Tasks` -> `Export...`.
4. Choose `No, do not export the private key`.
5. Select `DER encoded binary X.509 (.CER)` or `Base-64 encoded X.509 (.CER)`.
6. Save as `C:\temp\lt60mt-2station.cer`.

## 5. Install trust on another PC

On each target PC, follow these steps:

1. Copy `lt60mt-2station.cer` to the target PC.
2. Open `mmc.exe`.
3. Select `File` -> `Add/Remove Snap-in...`.
4. Choose `Certificates` and click `Add`.
5. Select `Computer account` and then `Local computer`.
6. Click `Finish` and `OK`.
7. In the left tree, expand `Certificates (Local Computer)`.
8. Right-click `Trusted Root Certification Authorities` -> `Certificates`.
9. Choose `All Tasks` -> `Import...`.
10. Follow the wizard and import `lt60mt-2station.cer`.

## 6. (Optional) also install under Trusted Publishers

For better code signing trust:

1. In the same MMC console, expand `Trusted Publishers` -> `Certificates`.
2. Right-click `Certificates` -> `All Tasks` -> `Import...`.
3. Import `lt60mt-2station.cer`.

## 7. Confirm the target PC trusts the certificate

1. Right-click the imported certificate in `Trusted Root Certification Authorities`.
2. Choose `Open`.
3. Verify that the certificate is valid and trusted.

## 8. Run the app on the target PC

Now run the signed `.msi` or `.exe` on the other PC.

If Windows still blocks it, make sure the certificate is installed in both:

- `Trusted Root Certification Authorities`
- `Trusted Publishers`

## 9. Important notes

- This is only for trusted internal machines.
- It will not make the app automatically trusted by external users.
- For public distribution, a real CA-issued code signing certificate is required.
- Keep the `.pfx` file and password secure.