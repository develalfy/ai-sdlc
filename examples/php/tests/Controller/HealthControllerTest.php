<?php
/** Single-file test for HealthController. Exit 0 = all pass. Run: php tests/Controller/HealthControllerTest.php */
declare(strict_types=1);
require __DIR__ . '/../../src/Controller/HealthController.php';
final class HealthControllerTest
{
    public static function main(): int
    {
        $c = (new HealthController())->healthz();
        $cases = [
            'returns 200 status'           => $c->getStatusCode() === 200,
            'returns application/json CT' => str_contains(strtolower($c->getHeaders()['Content-Type'] ?? ''), 'json'),
            'body has status=ok'           => (json_decode($c->getContent(), true)['status'] ?? null) === 'ok',
            'body has version=0.1.0'       => (json_decode($c->getContent(), true)['version'] ?? null) === '0.1.0',
        ];
        $pass = 0;
        foreach ($cases as $name => $ok) {
            echo ($ok ? 'PASS' : 'FAIL') . ' ' . $name . PHP_EOL;
            $pass += (int) $ok;
        }
        echo PHP_EOL . $pass . '/' . count($cases) . ' assertions passed.' . PHP_EOL;
        return $pass === count($cases) ? 0 : 1;
    }
}
exit(HealthControllerTest::main());
