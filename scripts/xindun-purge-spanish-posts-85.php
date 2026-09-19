<?php
/**
 * Plugin Name: Xindun Purge Spanish Posts Page85 Cache
 * Description: One-time localhost nginx purge for two Spanish news posts (page 85 fixes).
 * Version: 1.0.0
 */
if (!defined('ABSPATH')) {
    exit;
}

function xindun_purge_spanish_posts_85_request($url, $method, $host) {
    $response = wp_remote_request(
        $url,
        array(
            'method'      => $method,
            'timeout'     => 8,
            'redirection' => 0,
            'sslverify'   => false,
            'headers'     => array('Host' => $host),
        )
    );
    if (is_wp_error($response)) {
        return array('url' => $url, 'method' => $method, 'code' => $response->get_error_message());
    }
    return array(
        'url'   => $url,
        'method'=> $method,
        'code'  => wp_remote_retrieve_response_code($response),
        'cache' => wp_remote_retrieve_header($response, 'nginx-cache'),
    );
}

function xindun_purge_spanish_posts_85_run() {
    if (get_option('xindun_purge_spanish_posts_85_done') === '1.0.1') {
        return;
    }
    $host = parse_url(home_url(), PHP_URL_HOST);
    $paths = array(
        '/es-importante-el-inversor.html',
        '/los-inversores-off-grid-necesitan-estar-equipados-con-baterias.html',
    );
    $results = array();
    foreach ($paths as $path) {
        $results[] = xindun_purge_spanish_posts_85_request('https://127.0.0.1/purge' . $path, 'GET', $host);
        $results[] = xindun_purge_spanish_posts_85_request('http://127.0.0.1/purge' . $path, 'GET', $host);
        $results[] = xindun_purge_spanish_posts_85_request('https://127.0.0.1' . $path, 'PURGE', $host);
    }
    foreach (array(17441, 17447) as $id) {
        clean_post_cache($id);
        wp_cache_delete($id, 'posts');
    }
    if (function_exists('wp_cache_flush')) {
        wp_cache_flush();
    }
    update_option('xindun_purge_spanish_posts_85_log', $results, false);
    update_option('xindun_purge_spanish_posts_85_done', '1.0.1', false);
}

add_action('admin_init', 'xindun_purge_spanish_posts_85_run', 5);
register_activation_hook(__FILE__, 'xindun_purge_spanish_posts_85_run');

function xindun_purge_spanish_posts_85_notice() {
    if (!current_user_can('manage_options')) {
        return;
    }
    $log = get_option('xindun_purge_spanish_posts_85_log');
    if ($log) {
        echo '<div class="notice notice-info"><p><strong>Purge Spanish posts 85:</strong> '
            . esc_html(wp_json_encode($log))
            . '</p></div>';
    }
}
add_action('admin_notices', 'xindun_purge_spanish_posts_85_notice');
