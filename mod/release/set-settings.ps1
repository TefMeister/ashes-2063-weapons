# Writes the settings the 3D weapons were tuned with into the mod's own settings file.
# Called by "Play Ashes 2063 VR - 3D Weapons.bat" on every launch. Touches nothing else.
#   openvr_weaponRotate -50 : the gun angle in the hand (the engine default -40 points the guns up)
#   vr_two_handed_*         : the two-handed shotgun grip works at any hand distance
param([string]$Path)
$want = [ordered]@{
    'openvr_weaponRotate'        = '-50'
    'vr_two_handed_min_sep'      = '0'
    'vr_two_handed_max_disagree' = '180'
    'vr_two_handed_draw'         = 'true'
}
if (Test-Path -LiteralPath $Path) { $text = [IO.File]::ReadAllText($Path) } else { $text = "[GlobalSettings]`r`n" }
if ($text -notmatch '(?m)^\[GlobalSettings\]') { $text = "[GlobalSettings]`r`n" + $text }
foreach ($k in $want.Keys) {
    $line = "$k=$($want[$k])"
    if ($text -match "(?m)^$k=.*$") {
        $text = [regex]::Replace($text, "(?m)^$k=.*?(\r?)$", "$line`$1")
    } else {
        $text = ([regex]'(?m)^\[GlobalSettings\]\r?$').Replace($text, "[GlobalSettings]`r`n$line", 1)
    }
}
[IO.File]::WriteAllText($Path, $text)
