<?php

declare(strict_types=1);

namespace App\Controller;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

final class HealthController
{
    #[Route(
        path: '/api/v1/healthz',
        name: 'api_v1_healthz',
        methods: ['GET'],
    )]
    public function __invoke(): JsonResponse
    {
        return new JsonResponse(
            [
                'status' => 'ok',
                'version' => '0.1.0',
            ],
            Response::HTTP_OK,
        );
    }
}
