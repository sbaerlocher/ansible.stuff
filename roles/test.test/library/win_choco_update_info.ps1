
#!powershell

# Copyright: (c) 2018, Ansible Project
# Copyright: (c) 2018, Simon Baerlocher <s.baerlocher@sbaerlocher.ch>
# Copyright: (c) 2018, ITIGO AG <opensource@itigo.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Ansible.ModuleUtils.ArgvParser
#Requires -Module Ansible.ModuleUtils.CommandUtil
#Requires -Module Ansible.ModuleUtils.Legacy

$ErrorActionPreference = "Stop"
Set-StrictMode -Version 2.0

# Create a new result object
$result = @{
    changed  = $false
    packages = @()
}

$choco_app = Get-Command -Name choco.exe -CommandType Application -ErrorAction SilentlyContinue
if (-not $choco_app) {
    Fail-Json -obj $result -message "Failed to find Chocolatey installation, make sure choco.exe is in the PATH env value"
}

Function Get-ChocolateyUpdateInfo {

    param($choco_app)

    $command = Argv-ToString -arguments $choco_app.Path, "upgrade", "all", "-r"
    $res = Run-Command -command $command
    if ($res.rc -ne 0) {
        $result.stdout = $res.stdout
        $result.stderr = $res.stderr
        $result.rc = $res.rc
        Fail-Json -obj $result -message "Failed to list Chocolatey features, see stderr"
    }

    $packages_info = @{ }
    $res.stdout.Split("`r`n", [System.StringSplitOptions]::RemoveEmptyEntries) | select-object -skip 3 | Select-Object -SkipLast 3 | ForEach-Object {
        $packages_split = $_ -split "\|"

        $package_info = @{
            current   = $packages_split[1]
            available = $packages_split[2]
        }

        if ($packages_split[3] -eq "true") {            
            $packages_info.Add($packages_split[0], $package_info) > $null
        }
    }
    $result.packages = $packages_info
}

Get-ChocolateyUpdateInfo -choco_app $choco_app

# Return result
Exit-Json -obj $result
