$ContainerName = "myapi-container"

# .\Makefile.ps1 build
function Build-Image {
    docker build -t myapi .
}

#.\Makefile.ps1 run-webapp
function Run-WebApp {
    docker run -d --name $ContainerName -p 8000:8000 myapi
}

# .\Makefile.ps1 stop-webapp
function Stop-WebApp {
    docker stop $ContainerName
    docker rm $ContainerName
}

# .\Makefile.ps1 ps
function Show-RunningContainers {
    docker ps
}

# .\Makefile.ps1 host
function Start-Host {
    docker-compose up
}

# Define available commands
$Commands = @{
    "build"        = { Build-Image }
    "run-webapp"   = { Run-WebApp }
    "stop-webapp"  = { Stop-WebApp }
    "ps"           = { Show-RunningContainers }
    "host"         = { Start-Host }
}

# Parse arguments and execute corresponding function
if ($args.Count -gt 0) {
    $Command = $args[0]
    if ($Commands.ContainsKey($Command)) {
        & $Commands[$Command]
    } else {
        Write-Host "Unknown command: $Command"
    }
} else {
    Write-Host "Usage: .\script.ps1 [build | run-webapp | stop-webapp | ps | host]"
}