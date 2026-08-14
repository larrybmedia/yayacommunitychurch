import 'package:dio/dio.dart';

import '../models/event_model.dart';
import 'api_service.dart';

class EventService {
  final ApiService _apiService = ApiService();

  Future<List<EventModel>> getEvents() async {
    final Response response = await _apiService.get('/api/events');

    final List<dynamic> data = response.data;

    return data
        .map(
          (json) => EventModel.fromJson(
            json as Map<String, dynamic>,
          ),
        )
        .toList();
  }
}