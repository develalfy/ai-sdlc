<?php

declare(strict_types=1);

namespace App\Tests\Controller;

use App\Controller\HealthController;
use PHPUnit\Framework\TestCase;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;

final class HealthControllerTest extends TestCase
{
    public function testInvokeReturns200(): void
    {
        $response = (new HealthController())(/* request not needed */);

        self::assertSame(Response::HTTP_OK, $response->getStatusCode());
    }

    public function testInvokeReturnsJsonContentType(): void
    {
        $response = (new HealthController())();

        self::assertSame('application/json', $response->headers->get('Content-Type'));
    }

    public function testInvokeReturnsExpectedPayload(): void
    {
        /** @var JsonResponse $response */
        $response = (new HealthController())();

        self::assertSame(
            ['status' => 'ok', 'version' => '0.1.0'],
            json_decode((string) $response->getContent(), true, flags: JSON_THROW_ON_ERROR),
        );
    }

    public function testPayloadHasExactlyTwoKeys(): void
    {
        /** @var JsonResponse $response */
        $response = (new HealthController())();
        /** @var array<string, string> $data */
        $data = json_decode((string) $response->getContent(), true, flags: JSON_THROW_ON_ERROR);

        self::assertIsArray($data);
        self::assertCount(2, $data);
        self::assertSame('ok', $data['status']);
        self::assertSame('0.1.0', $data['version']);
    }
}
