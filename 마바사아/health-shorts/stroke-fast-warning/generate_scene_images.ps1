param(
  [string]$Project = "."
)

Add-Type -AssemblyName System.Drawing

$projectPath = Resolve-Path -LiteralPath $Project
$outDir = Join-Path $projectPath "assets\images"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$fontNum = New-Object System.Drawing.Font("Segoe UI", 78, [System.Drawing.FontStyle]::Bold)
$ink = [System.Drawing.Color]::FromArgb(26, 35, 43)
$deep = [System.Drawing.Color]::FromArgb(16, 25, 32)
$paper = [System.Drawing.Color]::FromArgb(241, 246, 242)
$teal = [System.Drawing.Color]::FromArgb(38, 119, 104)
$teal2 = [System.Drawing.Color]::FromArgb(76, 157, 139)
$red = [System.Drawing.Color]::FromArgb(194, 57, 48)
$amber = [System.Drawing.Color]::FromArgb(226, 171, 73)
$blue = [System.Drawing.Color]::FromArgb(54, 88, 131)

function Brush($color, $alpha = 255) {
  return New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb($alpha, $color.R, $color.G, $color.B))
}

function PenC($color, $width, $alpha = 255) {
  return New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb($alpha, $color.R, $color.G, $color.B), $width)
}

function Fill-RoundedRect($g, $brush, $x, $y, $width, $height, $radius) {
  $path = New-Object System.Drawing.Drawing2D.GraphicsPath
  $d = $radius * 2
  $path.AddArc($x, $y, $d, $d, 180, 90)
  $path.AddArc($x + $width - $d, $y, $d, $d, 270, 90)
  $path.AddArc($x + $width - $d, $y + $height - $d, $d, $d, 0, 90)
  $path.AddArc($x, $y + $height - $d, $d, $d, 90, 90)
  $path.CloseFigure()
  $g.FillPath($brush, $path)
  $path.Dispose()
}

function New-Canvas {
  $bmp = New-Object System.Drawing.Bitmap(1080, 1920)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $rect = New-Object System.Drawing.Rectangle(0, 0, 1080, 1920)
  $bg = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rect, [System.Drawing.Color]::FromArgb(246, 249, 246), [System.Drawing.Color]::FromArgb(218, 230, 224), 90)
  $g.FillRectangle($bg, $rect)
  $bg.Dispose()

  $wash = Brush $teal 18
  $g.FillEllipse($wash, -260, 1040, 720, 720)
  $g.FillEllipse($wash, 660, 180, 620, 620)
  $wash.Dispose()

  $panel = Brush ([System.Drawing.Color]::White) 115
  Fill-RoundedRect $g $panel 72 96 936 1500 58
  $panel.Dispose()

  $line = PenC $teal 4 42
  $g.DrawLine($line, 126, 1510, 954, 1510)
  $line.Dispose()
  return @($bmp, $g)
}

function Draw-Person($g, $x, $y, $scale, $faceDroop = $false) {
  $skin = Brush ([System.Drawing.Color]::FromArgb(229, 188, 153))
  $hair = Brush ([System.Drawing.Color]::FromArgb(45, 38, 34))
  $shirt = Brush $teal
  $shadow = Brush $deep 34
  $eye = Brush $deep
  $warn = PenC $red 12
  $neutral = PenC $deep 8 210

  $g.FillEllipse($shadow, $x + 25 * $scale, $y + 545 * $scale, 430 * $scale, 80 * $scale)
  Fill-RoundedRect $g $shirt ($x + 55 * $scale) ($y + 410 * $scale) (370 * $scale) (370 * $scale) (95 * $scale)
  $g.FillEllipse($hair, $x + 40 * $scale, $y, 400 * $scale, 430 * $scale)
  $g.FillEllipse($skin, $x + 10 * $scale, $y + 42 * $scale, 450 * $scale, 520 * $scale)
  $g.FillEllipse($eye, $x + 130 * $scale, $y + 240 * $scale, 28 * $scale, 28 * $scale)
  $g.FillEllipse($eye, $x + 296 * $scale, $y + 248 * $scale, 28 * $scale, 28 * $scale)

  if ($faceDroop) {
    $g.DrawArc($warn, $x + 214 * $scale, $y + 332 * $scale, 160 * $scale, 120 * $scale, 12, 122)
    $g.DrawLine($warn, $x + 330 * $scale, $y + 238 * $scale, $x + 382 * $scale, $y + 296 * $scale)
  } else {
    $g.DrawArc($neutral, $x + 165 * $scale, $y + 346 * $scale, 130 * $scale, 78 * $scale, 18, 145)
  }

  $skin.Dispose(); $hair.Dispose(); $shirt.Dispose(); $shadow.Dispose(); $eye.Dispose(); $warn.Dispose(); $neutral.Dispose()
}

function Draw-Phone($g, $x, $y, $show119 = $false) {
  $body = Brush $deep
  $screen = Brush $paper
  $redBrush = Brush $red
  $whiteBrush = Brush ([System.Drawing.Color]::White)
  Fill-RoundedRect $g $body $x $y 340 660 46
  Fill-RoundedRect $g $screen ($x + 28) ($y + 48) 284 548 32
  $g.FillEllipse($redBrush, $x + 110, $y + 245, 120, 120)
  if ($show119) {
    $g.DrawString("119", $fontNum, $redBrush, $x + 80, $y + 390)
  }
  $body.Dispose(); $screen.Dispose(); $redBrush.Dispose(); $whiteBrush.Dispose()
}

function Draw-MedicalGlow($g, $cx, $cy, $color) {
  $soft = Brush $color 35
  $line = PenC $color 9 185
  $g.FillEllipse($soft, $cx - 190, $cy - 190, 380, 380)
  $g.DrawEllipse($line, $cx - 120, $cy - 120, 240, 240)
  $g.DrawLine($line, $cx - 80, $cy, $cx + 80, $cy)
  $g.DrawLine($line, $cx, $cy - 80, $cx, $cy + 80)
  $soft.Dispose(); $line.Dispose()
}

function Draw-Scene($idx) {
  $pair = New-Canvas
  $bmp = $pair[0]
  $g = $pair[1]

  switch ($idx) {
    1 {
      Draw-Person $g 275 435 1.05 $true
      $mirrorPen = PenC $teal 7 90
      $g.DrawRectangle($mirrorPen, 210, 310, 650, 820)
      Draw-MedicalGlow $g 798 505 $red
      $mirrorPen.Dispose()
    }
    2 {
      Draw-Person $g 310 430 0.96 $false
      $goodArm = PenC $teal 30 230
      $weakArm = PenC $red 30 230
      $g.DrawLine($goodArm, 480, 940, 250, 720)
      $g.DrawLine($weakArm, 600, 940, 850, 1110)
      $g.FillEllipse((Brush $teal), 218, 690, 82, 82)
      $g.FillEllipse((Brush $red), 812, 1072, 82, 82)
      Draw-MedicalGlow $g 812 1106 $red
      $goodArm.Dispose(); $weakArm.Dispose()
    }
    3 {
      Draw-Person $g 105 520 0.82 $false
      Draw-Person $g 560 560 0.72 $false
      $bubble = Brush ([System.Drawing.Color]::White) 220
      Fill-RoundedRect $g $bubble 548 430 355 235 42
      $dot = Brush $red
      $g.FillEllipse($dot, 640, 522, 34, 34)
      $g.FillEllipse($dot, 715, 522, 34, 34)
      $g.FillEllipse($dot, 790, 522, 34, 34)
      Draw-MedicalGlow $g 725 530 $red
      $bubble.Dispose(); $dot.Dispose()
    }
    4 {
      Draw-Phone $g 370 480 $true
      $hand = Brush ([System.Drawing.Color]::FromArgb(229, 188, 153))
      Fill-RoundedRect $g $hand 238 980 430 150 62
      Draw-MedicalGlow $g 540 820 $red
      $hand.Dispose()
    }
    5 {
      $sofa = Brush $teal 220
      Fill-RoundedRect $g $sofa 150 990 780 260 56
      Draw-Person $g 248 470 0.92 $false
      $clockPen = PenC $amber 10 190
      $g.DrawEllipse($clockPen, 700, 410, 190, 190)
      $g.DrawLine($clockPen, 795, 505, 795, 445)
      $g.DrawLine($clockPen, 795, 505, 845, 535)
      Draw-MedicalGlow $g 795 505 $amber
      $sofa.Dispose(); $clockPen.Dispose()
    }
    6 {
      $colors = @($teal, $blue, $amber)
      for ($i = 0; $i -lt 3; $i++) {
        $y = 430 + $i * 300
        $b = Brush $colors[$i] 222
        Fill-RoundedRect $g $b 230 $y 620 210 44
        $icon = Brush ([System.Drawing.Color]::White) 235
        if ($i -eq 0) {
          $g.FillEllipse($icon, 305, $y + 42, 125, 125)
          $g.FillEllipse((Brush $deep 180), 342, $y + 94, 14, 14)
          $g.FillEllipse((Brush $deep 180), 383, $y + 96, 14, 14)
        } elseif ($i -eq 1) {
          $armPen = PenC ([System.Drawing.Color]::White) 30 235
          $g.DrawLine($armPen, 320, $y + 115, 500, $y + 55)
          $g.DrawLine($armPen, 500, $y + 55, 680, $y + 145)
          $armPen.Dispose()
        } else {
          Fill-RoundedRect $g $icon 310 ($y + 55) 250 100 32
          $g.FillEllipse($icon, 545, $y + 130, 55, 55)
        }
        $b.Dispose(); $icon.Dispose()
      }
    }
    7 {
      Draw-Phone $g 365 440 $true
      $light = Brush $red 38
      $g.FillEllipse($light, 230, 290, 620, 620)
      Draw-MedicalGlow $g 535 785 $red
      $light.Dispose()
    }
    8 {
      $card = Brush ([System.Drawing.Color]::White) 235
      Fill-RoundedRect $g $card 190 410 700 760 58
      $accentPen = PenC $teal 16 210
      $checkPen = PenC $red 16 230
      for ($i = 0; $i -lt 3; $i++) {
        $y = 560 + $i * 165
        $g.DrawEllipse($accentPen, 290, $y, 78, 78)
        $g.DrawLine($checkPen, 308, $y + 40, 332, $y + 64)
        $g.DrawLine($checkPen, 332, $y + 64, 358, $y + 18)
        $bar = Brush $ink 135
        Fill-RoundedRect $g $bar 420 ($y + 18) 330 34 17
        $bar.Dispose()
      }
      Draw-Phone $g 650 930 $true
      Draw-MedicalGlow $g 540 1230 $teal
      $card.Dispose(); $accentPen.Dispose(); $checkPen.Dispose()
    }
  }

  $vignette = PenC $deep 44 20
  $g.DrawRectangle($vignette, 22, 22, 1036, 1876)
  $vignette.Dispose()

  $path = Join-Path $outDir ("scene-{0:D2}.png" -f $idx)
  $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose()
  $bmp.Dispose()
}

for ($i = 1; $i -le 8; $i++) {
  Draw-Scene $i
}

Write-Output $outDir
