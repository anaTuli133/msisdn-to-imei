<?php
// ---- CONFIG ----
// ----Change IP of URL Accordingly ------
define('API_URL', 'http://127.0.0.1:8000/api/msisdn-to-imei');
define('USERNAME', 'rahi');
define('PASSWORD', '5096');

// ---- INPUT (can be dynamic later) ----
$msisdn = $argv[1] ?? '8801550155096';
//$start  = $argv[2] ?? date('Y-m-d', strtotime('-1 day'));
//$end    = $argv[3] ?? date('Y-m-d');

// ---- API CALL ----
$payload = json_encode([
    "msisdn" => [$msisdn]
    //"start_date" => $start,
    //"end_date" => $end
]);

$ch = curl_init(API_URL);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $payload,
    CURLOPT_USERPWD => USERNAME . ":" . PASSWORD,
    CURLOPT_HTTPAUTH => CURLAUTH_BASIC,
    CURLOPT_HTTPHEADER => ['Content-Type: application/json']
]);

$response = curl_exec($ch);
$error = curl_error($ch);
//curl_close($ch);

if ($error) {
    echo "Error: $error\n";
    exit;
}

$data = json_decode($response, true);

// ---- OUTPUT ----
echo "Requested by: " . ($data['requested_by'] ?? 'N/A') . "\n";
echo "Total Records: " . ($data['count'] ?? 0) . "\n";

foreach ($data['data'] ?? [] as $row) {
    echo "{$row['IMEI']}\n"; #{$row['DATE_VALUE']} | {$row['MSISDN']} | 
}
