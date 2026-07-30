$ErrorActionPreference = 'Stop'

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = 'C:\Users\lzx10\AppData\Local\Python\pythoncore-3.14-64\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    throw "Python executable was not found: $python"
}

& $python (Join-Path $scriptRoot 'homekit_mdns_advertiser.py')
exit $LASTEXITCODE
