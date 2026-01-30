import 'package:myapp/userInterfaces/UserLoginAndSubscription/Doctor.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
/*class SearchDoctorService {
  static Future<List<Doctor>> fetchDoctors(String currentPosition, String v) async {
   String  query = v = v.trim().toLowerCase();
    final response = await http.get(Uri.parse(


        'http://192.168.1.28:5100/api/searchDoctors?mycurrentposition=$currentPosition&v=$query'));

   if (response.statusCode == 200) {
     final Map<String, dynamic> decoded = jsonDecode(response.body);
     final dynamic data = decoded['msg'];
     if ( data is List) {
       return data.map((json) => Doctor.fromJson(json)).toList();
     }
     else {
       throw Exception("$data not a list ");
     }
   } else {
     throw Exception('Failed to load doctors');
   }
  }
}
*/

class SearchDoctorService {
  static Future<List<Doctor>> fetchDoctors(String currentPosition, String v) async {
    String query = v.trim().toLowerCase();
    final response = await http.get(Uri.parse(
        'http://192.168.43.128:5100/api/searchDoctors?mycurrentposition=$currentPosition&v=$query'));
    if (response.statusCode == 200) {
      final Map<String, dynamic> decoded = jsonDecode(response.body);

      // access the nested list
      final dynamic data = decoded['msgFinal']?['msg'];

      if (data is List) {
        return data.map((json) => Doctor.fromJson(json)).toList();
      } else {
        throw Exception("$data not a list");
      }
    } else {
      throw Exception('Failed to load doctors');
    }
  }
}
