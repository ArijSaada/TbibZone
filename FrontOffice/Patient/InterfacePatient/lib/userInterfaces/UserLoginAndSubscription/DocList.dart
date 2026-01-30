import 'dart:convert';
import 'package:http/http.dart' as http;
import 'Doctor.dart';

class DoctorService {
  static Future<List<Doctor>> fetchDoctors(String address) async {
    final uri = Uri.parse(
      'http://192.168.43.128:5100/api/doctors?mycurrentposition=${Uri.encodeComponent(address)}',
    );

    final response = await http.get(uri).timeout(Duration(seconds: 20));


    if (response.statusCode == 200) {
      final decoded = jsonDecode(response.body) as Map<String, dynamic>;
      final dynamic body = decoded['msg'] ;
      if (body is List) {
        // Ensure it's a List and map it to List<Doctor>
        if (body.isNotEmpty) {
          return body.map<Doctor>((json) => Doctor.fromJson(json)).toList();
        }
        else {
          return[];

        }
      }
      else {
        throw Exception("API response is not a list $body");
      }
    } else {
      throw Exception("Failed to load doctors: ${response.statusCode}");
    }
  }
}
