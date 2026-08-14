class EventModel {
  final int id;
  final String title;
  final String date;

  EventModel({
    required this.id,
    required this.title,
    required this.date,
  });

  factory EventModel.fromJson(Map<String, dynamic> json) {
    return EventModel(
      id: json['id'],
      title: json['title'] ?? '',
      date: json['date'] ?? '',
    );
  }
}