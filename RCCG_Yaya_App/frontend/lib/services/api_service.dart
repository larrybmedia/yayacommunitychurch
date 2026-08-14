import 'package:dio/dio.dart';

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:5000';

  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      headers: {
        'Content-Type': 'application/json',
      },
    ),
  );

  Future<Response> get(String endpoint) async {
    return await _dio.get(endpoint);
  }

  Future<Response> post(
    String endpoint, {
    dynamic data,
  }) async {
    return await _dio.post(
      endpoint,
      data: data,
    );
  }
}