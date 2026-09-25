# Windows Code Signing Instructions

This document explains how to sign the desktop app executable and MSI installer for `L-T_60MT_2Station`.

## Prerequisites

1. Install the Windows 10 SDK signing tools.
   - Make sure `Windows SDK Signing Tools for Desktop Apps` is installed.
   - The signing tool will be available at:
     `C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\signtool.exe`

2. Obtain a Windows code signing certificate.
   - This must be a real code signing certificate from a trusted CA, or an internal company code signing certificate.
   - The certificate file should be in `.pfx` format.

3. Know the `.pfx` password.
   - The `.pfx` file is protected with a password, which is required to sign.

## Files to sign

- `D:\L-T_60MT_2Station\desktop\L-T_60MT_2STATION\src-tauri\target\release\l-t-60mt-2station.exe`
- `D:\L-T_60MT_2Station\desktop\L-T_60MT_2STATION\src-tauri\target\release\bundle\msi\l-t-60mt-2station_0.1.0_x64_en-US.msi`

## PowerShell signing command

Update the following command with your certificate path, password, and SDK version folder.

```powershell
$cert = "C:\path\to\yourcert.pfx"
$pass = "YourPfxPassword"
$tstamp = "http://timestamp.digicert.com"
$signtool = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.28000.0\x64\signtool.exe"

& $signtool sign /f $cert /p $pass /fd SHA256 /tr $tstamp /td SHA256 \
  "D:\L-T_60MT_2Station\desktop\L-T_60MT_2STATION\src-tauri\target\release\l-t-60mt-2station.exe"

& $signtool sign /f $cert /p $pass /fd SHA256 /tr $tstamp /td SHA256 \
  "D:\L-T_60MT_2Station\desktop\L-T_60MT_2STATION\src-tauri\target\release\bundle\msi\l-t-60mt-2station_0.1.0_x64_en-US.msi"
```

## Verification

After signing, verify both files have a digital signature:

1. Right-click the file.
2. Choose `Properties`.
3. Open the `Digital Signatures` tab.

## Notes

- If the certificate is expired or invalid, signing will fail.
- If you want the signed file to remain valid after certificate expiration, use timestamp signing as shown above.
- If your company uses an internal CA, request a code signing certificate from IT/security.

## Buying a code signing certificate

A `.pfx` certificate must be issued by a trusted code signing certificate authority (CA).

### Recommended providers

- DigiCert
- GlobalSign
- Sectigo
- SSL.com
- GoDaddy

### What to buy

- A **standard code signing certificate** is usually enough for a small company.
- If you want the safest SmartScreen experience, use an **EV code signing certificate**, but it is more expensive.
- Most certificates are sold with a **1-year** or **2-year** renewal option.

### Cost and renewal

- Typical cost is around **$100–$400 per year** for a standard code signing cert.
- You can also buy multi-year validity if the vendor supports it.
- The certificate itself typically expires and must be renewed.
- Timestamp signing keeps old signed files valid even after the cert expires.

### If you do not want to purchase yet

- You can create a **self-signed certificate** for internal testing, but it will not be trusted by other computers or SmartScreen.
- For real distribution, a trusted CA certificate is required.

## Exporting `.pfx`

If your company already has a code signing certificate installed in Windows, ask IT to provide it as a `.pfx` file.

1. Open `certmgr.msc` or the Windows Certificate Manager.
2. Find the code signing certificate under `Personal` or the appropriate store.
3. Export it as a `.pfx` file, including the private key.
4. Keep the `.pfx` password secure.

## Optional: add a post-build signing step

This guide can be used manually, or you can automate signing after the desktop build completes.
