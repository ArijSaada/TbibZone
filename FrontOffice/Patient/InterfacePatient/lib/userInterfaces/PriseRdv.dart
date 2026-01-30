import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:table_calendar/table_calendar.dart';
import 'dart:convert';

class AppointmentPage extends StatefulWidget {
  final String userEmail;
  final String nomDoc;
  final String prenomDoc;

  const AppointmentPage({
    Key? key,
    required this.userEmail,
    required this.nomDoc,
    required this.prenomDoc,
  }) : super(key: key);

  @override
  _AppointmentPageState createState() => _AppointmentPageState();
}

class _AppointmentPageState extends State<AppointmentPage> {
  DateTime _selectedDay = DateTime.now();
  Map<String, List<String>> _slotsByDate = {
  }; // all fetched slots grouped by day
  List<String> _availableTimes = [];
  String? _selectedTime;

  @override
  void initState() {
    super.initState();
    _fetchAllAvailableTimes();
  }

  Future<void> _fetchAllAvailableTimes() async {
    final nom = widget.nomDoc;
    final prenom = widget.prenomDoc;

    final url = Uri.parse('http://192.168.43.128:5400/disponibilite');


    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'nom_doc': nom,
          'prenom': prenom,
        }),
      );


      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("Data received")));
        final Map<String, dynamic> data = json.decode(response.body);
        final List<dynamic> slots = data['available_slots'];

        final Map<String, List<String>> grouped = {};

        for (var slot in slots) {
          final parts = slot.split(" ");
          if (parts.length == 2) {
            final date = parts[0];
            final time = parts[1];
            grouped.putIfAbsent(date, () => []).add(time);
          }
        }

        setState(() {
          _slotsByDate = grouped;
          _updateAvailableTimes(); // based on initial _selectedDay
        });
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Failed to receive data")),
        );

        print("Erreur serveur: ${response.statusCode}");
      }
    } catch (e) {
      print("Erreur lors du chargement: $e");
    }
  }

  void _updateAvailableTimes() {
    final formattedDate = _selectedDay.toIso8601String().split("T")[0];
    final times = _slotsByDate[formattedDate] ?? [];

    setState(() {
      _availableTimes = times;
      _selectedTime = null;
    });
  }

  void _bookAppointment() async {
    if (_selectedTime == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Veuillez choisir une heure")),
      );
      return;
    }

    final appointmentDate =
        "${_selectedDay.toIso8601String().split('T')[0]} $_selectedTime:00";

    final body = jsonEncode({
      "nom_doc": widget.nomDoc,
      "prenom_doc": widget.prenomDoc,
      "Mail": widget.userEmail,
      "appointment_date": appointmentDate,
    });

    final url = Uri.parse("http://192.168.43.128:5400/rdvPatient");

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: body,
      );

      final responseData = json.decode(response.body);

      if (response.statusCode == 200 && responseData["success"] == true) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("✅ ${responseData["msg"]}"),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("❌ ${responseData["msg"] ?? "Erreur inconnue"}"),
            backgroundColor: Colors.red,
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Erreur réseau : $e"),
          backgroundColor: Colors.red,
        ),
      );
    }


    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          "Rendez-vous pris avec Dr. ${widget.nomDoc} ${widget
              .prenomDoc} à $_selectedTime le ${_selectedDay
              .toLocal()
              .toString()
              .split(" ")[0]}",
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Prendre un rendez-vous"),
        backgroundColor: Colors.green.shade200,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TableCalendar(
              focusedDay: _selectedDay,
              firstDay: DateTime.now(),
              lastDay: DateTime.now().add(Duration(days: 60)),
              selectedDayPredicate: (day) => isSameDay(day, _selectedDay),
              onDaySelected: (selectedDay, focusedDay) {
                setState(() {
                  _selectedDay = selectedDay;
                  _updateAvailableTimes(); // Update list for selected day
                });
              },
            ),
            SizedBox(height: 20),
            Text(
              "Heures disponibles pour ${_selectedDay.toLocal().toString().split(" ")[0]} :",
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            Wrap(
              spacing: 10,
              children: _availableTimes.map((time) {
                final isSelected = time == _selectedTime;
                return ChoiceChip(
                  label: Text(time),
                  selected: isSelected,
                  onSelected: (_) {
                    setState(() {
                      _selectedTime = time;
                    });
                  },
                  selectedColor: Colors.green.shade300,
                );
              }).toList(),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed:() {
                _bookAppointment();

                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text("$_selectedDay + $_selectedTime"),),);
              },
              child: Text("Réserver"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green.shade600,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

