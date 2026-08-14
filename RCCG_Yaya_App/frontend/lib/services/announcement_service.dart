import 'package:dio/dio.dart';

import '../models/announcement_model.dart';
import 'api_service.dart';

class AnnouncementService {
  final ApiService _apiService = ApiService();

  Future<List<AnnouncementModel>> getAnnouncements() async {
    final Response response =
        await _apiService.get('/api/announcements');

    final List<dynamic> data = response.data;

    return data
        .map(
          (json) => AnnouncementModel.fromJson(
            json as Map<String, dynamic>,
          ),
        )
        .toList();
  }
}