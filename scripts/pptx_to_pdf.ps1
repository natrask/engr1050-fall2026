<#
.SYNOPSIS
  Export every .pptx under NewMaterial/ to a sibling .pdf using PowerPoint.

.DESCRIPTION
  Each lecture links both a PPT and a PDF copy of its slides: the PPT is what
  Nat downloads in the lecture room, the PDF is what students view in the
  browser. This keeps the PDF in sync after editing a deck.

  Skips decks whose .pdf is already newer than the .pptx unless -Force.

.EXAMPLE
  powershell -File scripts/pptx_to_pdf.ps1
  powershell -File scripts/pptx_to_pdf.ps1 -Force
#>
param([switch]$Force)

$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot -Parent) 'NewMaterial'
$decks = Get-ChildItem -Path $root -Filter *.pptx -Recurse -File

if (-not $decks) { "No .pptx files found under NewMaterial/"; exit 0 }

$todo = foreach ($d in $decks) {
  $pdf = [IO.Path]::ChangeExtension($d.FullName, '.pdf')
  if ($Force -or -not (Test-Path $pdf) -or (Get-Item $pdf).LastWriteTime -lt $d.LastWriteTime) {
    [pscustomobject]@{ Pptx = $d.FullName; Pdf = $pdf; Name = $d.Name }
  }
}
if (-not $todo) { "All PDFs are up to date."; exit 0 }

$pp = New-Object -ComObject PowerPoint.Application
try {
  foreach ($t in $todo) {
    $pres = $pp.Presentations.Open($t.Pptx, $true, $false, $false)  # ReadOnly, no window
    $pres.SaveAs($t.Pdf, 32)                                        # 32 = ppSaveAsPDF
    $pres.Close()
    "exported $($t.Name) -> $([IO.Path]::GetFileName($t.Pdf))"
  }
} finally {
  $pp.Quit()
  [Runtime.InteropServices.Marshal]::ReleaseComObject($pp) | Out-Null
}
