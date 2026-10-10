$port = 5173
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Prefixes.Add("http://127.0.0.1:$port/")

try {
    $listener.Start()
    Write-Host "🌿 PCOS Saathi Local Server running at: http://localhost:$port/" -ForegroundColor Green
    Write-Host "Open http://localhost:$port/ in your browser." -ForegroundColor Cyan
} catch {
    Write-Host "Error starting listener on port $port : $_" -ForegroundColor Red
    exit 1
}

$previewPath = Join-Path $PSScriptRoot "preview.html"

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        if (Test-Path $previewPath) {
            $buffer = [System.IO.File]::ReadAllBytes($previewPath)
            $response.ContentType = "text/html; charset=utf-8"
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        } else {
            $response.StatusCode = 404
        }
        $response.Close()
    } catch {
        # Handle client disconnect or listener stop
    }
}
