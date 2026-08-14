import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class ApiService {
  final http.Client _client = http.Client();

  Uri _uri(String endpoint) {
    return Uri.parse('${ApiConfig.baseUrl}$endpoint');
  }

  Future<http.Response> get(String endpoint) {
    return _client.get(_uri(endpoint));
  }

  Future<http.Response> post(
    String endpoint, {
    Object? body,
    Map<String, String>? headers,
  }) {
    return _client.post(_uri(endpoint), body: body, headers: headers);
  }
}
