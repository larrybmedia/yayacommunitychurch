class AnnouncementModel {
  final int id;
  final String title;
  final String content;
  final String? imageFilename;
  final String? videoUrl;
  final int? adminId;
  final DateTime? dateCreated;

  AnnouncementModel({
    required this.id,
    required this.title,
    required this.content,
    this.imageFilename,
    this.videoUrl,
    this.adminId,
    this.dateCreated,
  });

  factory AnnouncementModel.fromJson(Map<String, dynamic> json) {
    return AnnouncementModel(
      id: json['id'] ?? 0,
      title: json['title'] ?? '',
      content: json['content'] ?? '',
      imageFilename: json['image_filename'],
      videoUrl: json['video_url'],
      adminId: json['admin_id'],
      dateCreated: json['date_created'] != null
          ? DateTime.tryParse(json['date_created'].toString())
          : null,
    );
  }
}