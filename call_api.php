<?php
/**
 * MSISDN to IMEI API — PHP Example
 * how 3rd party will call */

// ----  credentials ----
define('API_URL',  'http://192.168.8.164:8000/api/msisdn-to-imei');
define('USERNAME', 'rahi'); 
define('PASSWORD', '5096');   

function getMsisdnToImei(array $msisdn_list): array
{
    $payload = json_encode([
        'msisdn'     => $msisdn_list,
        //'start_date' => $start_date,
        //'end_date'   => $end_date,
    ]);

    $ch = curl_init(API_URL);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => $payload,
        CURLOPT_USERPWD        => USERNAME . ':' . PASSWORD,  // Basic Auth
        CURLOPT_HTTPAUTH       => CURLAUTH_BASIC,
        CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
        CURLOPT_TIMEOUT        => 60,
    ]);

    $response  = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    //curl_close($ch);

    if ($http_code === 401) {
        return ['error' => 'Invalid username or password', 'code' => 401];
    }

    if ($http_code !== 200) {
        return ['error' => 'API error', 'code' => $http_code];
    }

    return json_decode($response, true);
}

// ---- Example Usage ----
$result = getMsisdnToImei(
    msisdn_list: ['8801550155096'],
    // start_date:  '2026-04-10',
    // end_date:    '2026-04-11'
);

echo "<pre>";

if (isset($result['error'])) {
    echo "Error: " . $result['error'];
} else {
    print_r($result); 

    echo "\n\nFormatted Output:\n";

    echo "Requested by: " . $result['requested_by'] . "\n";
    echo "Total Records: " . $result['count'] . "\n";

    foreach ($result['data'] as $row) {
        echo "Date: {$row['DATE_VALUE']} | MSISDN: {$row['MSISDN']} | IMEI: {$row['IMEI']}\n";
    }
}

echo "</pre>";
?>