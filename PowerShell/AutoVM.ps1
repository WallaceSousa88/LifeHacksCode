# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

$NomeVM = "win10"
$CaminhoVM = "C:\VM\VM"
$CaminhoHD = "C:\VM\HD"
$CaminhoISO = "C:\ISO\Win10.iso"
$TamanhoHDGB = 100
$MemoriaRAMGB = 8
$NumProcessadores = 10
$GeracaoVM = 2  # 1 ou 2

Write-Host "Iniciando criacao da VM..." -ForegroundColor Cyan

if (!(Test-Path $CaminhoVM)) {
    New-Item -ItemType Directory -Path $CaminhoVM | Out-Null
    Write-Host "Diretorio de configuracao criado: $CaminhoVM"
}

if (!(Test-Path $CaminhoHD)) {
    New-Item -ItemType Directory -Path $CaminhoHD | Out-Null
    Write-Host "Diretorio de disco criado: $CaminhoHD"
}

$CaminhoVHDX = Join-Path $CaminhoHD "$NomeVM.vhdx"
$TamanhoHDBytes = $TamanhoHDGB * 1GB
New-VHD -Path $CaminhoVHDX -SizeBytes $TamanhoHDBytes -Dynamic | Out-Null
Write-Host "Disco virtual criado: $CaminhoVHDX"

$MemoriaRAMBytes = $MemoriaRAMGB * 1GB
New-VM -Name $NomeVM -MemoryStartupBytes $MemoriaRAMBytes -Generation $GeracaoVM -VHDPath $CaminhoVHDX -Path $CaminhoVM | Out-Null
Write-Host "VM criada com sucesso: $NomeVM (Geracao $GeracaoVM)"

Set-VMProcessor -VMName $NomeVM -Count $NumProcessadores
Write-Host "Processadores configurados: $NumProcessadores"

Set-VMDvdDrive -VMName $NomeVM -Path $CaminhoISO
Write-Host "Imagem ISO conectada: $CaminhoISO"

$Switch = Get-VMSwitch | Select-Object -First 1
if ($Switch) {
    Add-VMNetworkAdapter -VMName $NomeVM -SwitchName $Switch.Name
    Write-Host "Adaptador de rede conectado ao switch: $($Switch.Name)"
} else {
    Write-Host "Nenhum switch virtual encontrado. Adaptador de rede nao adicionado." -ForegroundColor Yellow
}

Start-VM -Name $NomeVM
Write-Host "VM iniciada. Prossiga com a instalacao manual do Windows." -ForegroundColor Green
