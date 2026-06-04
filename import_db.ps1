$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$mysqlCmd = "mysql"
$mysqlArgs = @(
    "-u", "root",
    "-p123456",
    "--default-character-set=utf8mb4",
    "pbl6"
)

$sqlPath = "C:\Users\Administrator\Desktop\新建文件夹\pbl6.sql"

try {
    $sqlContent = [System.IO.File]::ReadAllText($sqlPath, [System.Text.Encoding]::UTF8)
    $sqlBytes = [System.Text.Encoding]::UTF8.GetBytes($sqlContent)

    $tempFile = [System.IO.Path]::GetTempFileName() + ".sql"
    [System.IO.File]::WriteAllBytes($tempFile, $sqlBytes)

    $process = Start-Process -FilePath $mysqlCmd -ArgumentList $mysqlArgs -NoNewWindow -Wait -PassThru -RedirectStandardInput $tempFile

    if ($process.ExitCode -eq 0) {
        Write-Host "Database imported successfully!"
    } else {
        Write-Host "Error importing database. Exit code: $($process.ExitCode)"
    }

    Remove-Item $tempFile -Force -ErrorAction SilentlyContinue

} catch {
    Write-Host "Error: $_"
}