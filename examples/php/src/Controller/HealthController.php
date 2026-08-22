<?php
/**
 * Synthetic Symfony-style controller (no vendor tree required).
 *
 * Runs on PHP 8.4+ built-ins only. No Symfony autoloader, no composer.
 * Mirrors the Symfony 6.x JsonResponse contract: a constructor that
 * takes ($data, $status, $headers) and a getContent() method that
 * returns the JSON string.
 */
declare(strict_types=1);

final class HealthController
{
    public function healthz(): JsonResponse
    {
        return new JsonResponse(['status' => 'ok', 'version' => '0.1.0']);
    }
}

final class JsonResponse
{
    /** @param array<string,mixed> $headers */
    public function __construct(
        private readonly mixed $data,
        private readonly int $status = 200,
        private readonly array $headers = [],
    ) {}

    public function getStatusCode(): int
    {
        return $this->status;
    }

    public function getContent(): string
    {
        $flags = JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE;
        $body = json_encode($this->data, $flags);
        if ($body === false) {
            throw new RuntimeException('JsonResponse: failed to encode payload.');
        }
        return $body;
    }

    /** @return array<string,string> */
    public function getHeaders(): array
    {
        $base = ['Content-Type' => 'application/json'];
        return array_merge($base, $this->headers);
    }
}
