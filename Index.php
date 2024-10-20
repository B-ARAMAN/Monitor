<?php
// config.php
$config = [
    'site_url' => 'phonoverse.x10.bz',
    'log_file' => 'monitor_log.json',
    'locations' => [
        'NA' => 'North America',
        'EU' => 'Europe',
        'AS' => 'Asia'
    ]
];

// Read the log file
$log_data = [];
if (file_exists($config['log_file'])) {
    $log_data = json_decode(file_get_contents($config['log_file']), true);
}

// Get the latest entry
$latest_status = end($log_data);

// Calculate uptime
function calculateUptime($log_data) {
    if (empty($log_data)) return 0;
    $up_count = count(array_filter($log_data, function($entry) {
        return $entry['status'] == 1;
    }));
    return round(($up_count / count($log_data)) * 100, 2);
}

$uptime = calculateUptime($log_data);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor - <?php echo $config['site_url']; ?></title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        /* Styles similar to your provided HTML */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SERVER MONITOR</h1>
            <p>Monitoring: <?php echo $config['site_url']; ?></p>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h2><i class="fas fa-server"></i>Current Status</h2>
                <div class="metric">
                    <span>Status</span>
                    <span>
                        <span class="status-indicator <?php echo $latest_status['status'] == 1 ? 'status-up' : 'status-down'; ?>"></span>
                        <?php echo $latest_status['status'] == 1 ? 'Online' : 'Offline'; ?>
                    </span>
                </div>
                <div class="metric">
                    <span>Response Time</span>
                    <span><?php echo $latest_status['response_time']; ?>ms</span>
                </div>
                <div class="metric">
                    <span>24h Uptime</span>
                    <span><?php echo $uptime; ?>%</span>
                </div>
            </div>
            
            <div class="card">
                <h2><i class="fas fa-chart-line"></i>System Metrics</h2>
                <div class="metric">
                    <span>Memory Usage</span>
                    <span><?php echo round($latest_status['memory_usage'] / 1024 / 1024, 2); ?> MB</span>
                </div>
                <div class="metric">
                    <span>CPU Load</span>
                    <span><?php echo $latest_status['cpu_load']; ?></span>
                </div>
                <div class="metric">
                    <span>Disk Space</span>
                    <span><?php echo round($latest_status['disk_usage'], 2); ?>% free</span>
                </div>
            </div>
            
            <div class="card">
                <h2><i class="fas fa-globe"></i>Regional Response Times</h2>
                <?php foreach($latest_status['regional_latency'] as $region => $latency): ?>
                <div class="metric">
                    <span><?php echo $config['locations'][$region]; ?></span>
                    <span><?php echo $latency; ?>ms</span>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>
</body>
</html>
