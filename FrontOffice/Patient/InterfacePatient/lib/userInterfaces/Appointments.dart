import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


class AppointmentsScreen extends StatefulWidget {
  final String username;

  AppointmentsScreen({required this.username});

  @override
  _AppointmentsScreenState createState() => _AppointmentsScreenState();
}

class _AppointmentsScreenState extends State<AppointmentsScreen> {
  late Future<List<dynamic>> _appointmentsFuture;

  @override
  void initState() {
    super.initState();
    _appointmentsFuture = fetchAppointments(context, widget.username);
  }

  void _refreshAppointments() {
    setState(() {
      _appointmentsFuture = fetchAppointments(context, widget.username);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Appointments for ${widget.username}'),
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _appointmentsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (snapshot.hasData) {
            var appointments = snapshot.data!;
            if (appointments.isEmpty) {
              Future.delayed(Duration.zero, () {
                showDialog(
                  context: context,
                  builder: (BuildContext context) {
                    return AlertDialog(
                      title: const Text('No Appointments'),
                      content: const Text('You have no appointments scheduled.'),
                      actions: [
                        TextButton(
                          onPressed: () {
                            Navigator.pushNamed(context, '/using',
                                arguments: {'username': widget.username});
                          },
                          child: const Text('Close'),
                        ),
                      ],
                    );
                  },
                );
              });
              return Center(child: Text('No appointments available.'));
            }
            return ListView.builder(
              itemCount: appointments.length,
              itemBuilder: (context, index) {
                var appointment = appointments[index];
                return Card(
                  margin: EdgeInsets.all(10),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  child: ListTile(
                    leading: Icon(Icons.calendar_today, color: Colors.blue),
                    title: Text(
                      ((appointment['nom_doc'] ?? '') + ' ' + (appointment['prenom_doc'] ?? 'No title provided')).trim(),
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text('${appointment['appointment_date']}'),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          appointment['status'] ?? 'Unknown status',
                          style: TextStyle(
                            color: appointment['status'] == 'Upcoming'
                                ? Colors.green
                                : appointment['status'] == 'Completed'
                                ? Colors.grey
                                : Colors.red,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        IconButton(
                          icon: Icon(Icons.delete, color: Colors.red),
                          onPressed: () async {
                            final url = Uri.parse('http://192.168.43.128:5400/delrdvPatient');
                            final body = json.encode({
                              "nom_doc": appointment['nom_doc'],
                              "prenom_doc": appointment['prenom_doc'],
                              "Mail": widget.username,
                              "appointment_date": appointment['appointment_date'],
                            });

                            try {
                              final response = await http.delete(
                                url,
                                headers: {"Content-Type": "application/json"},
                                body: body,
                              );

                              if (response.statusCode == 200) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(content: Text("Appointment deleted successfully")),
                                );
                                _refreshAppointments();
                              } else {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(content: Text("Failed to delete. Code: ${response.statusCode}")),
                                );
                              }
                            } catch (e) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text("Error: $e")),
                              );
                            }
                          },
                        ),
                        IconButton(
                          icon: Icon(Icons.edit),
                          onPressed: () {
                            String newnom_doc = '';
                            String newprenom_doc = '';
                            String newappointment_date = '';
                            showDialog(context: context, builder:(context){
                              return AlertDialog(
                                title: Text('Modifier_rendez-vous'),
                                content: Column(mainAxisSize: MainAxisSize.min,
                                    children: [
                                      TextFormField (
                                        decoration: InputDecoration(labelText: 'Nom médecin'),
                                        onChanged: (value) {
                                          newnom_doc = value;
                                        },


                                      ),
                                      TextFormField (
                                        decoration: InputDecoration(labelText: 'prenom médecin'),
                                        onChanged: (value) {
                                          newprenom_doc = value;
                                        },


                                      ),
                                      TextFormField (
                                        decoration: InputDecoration(labelText: 'date temps', hintText: appointment['appointment_date']),
                                        onChanged: (value) {
                                          newappointment_date = value;
                                        },


                                      ),
                                      ElevatedButton(onPressed: () async{
                                        final urlModif = Uri.parse('http://192.168.43.128:5400/patient/modify_rdv');
                                        final bodymodifparams = {
                                          'Mail': widget.username,
                                          'nom_doc' : appointment['nom_doc'],
                                          'prenom_doc': appointment['prenom_doc'],
                                          'appointment_date': appointment['appointment_date'],
                                          'newnom_doc' : newnom_doc,
                                          'newprenom_doc': newprenom_doc,
                                          'newappointment_date' : newappointment_date



                                        };
                                        try {
                                          final modifresponse = await http.put(urlModif,
                                          headers:
                                          {
                                            'Content-type':'application/json'
                                          },
                                              body: json.encode(bodymodifparams),
                                          );
                                          if (modifresponse.statusCode == 200) {
                                            ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erreur: ${modifresponse.statusCode} - ${modifresponse.body}')));

                                          }
                                          else {
                                            ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('${modifresponse}')));
                                          }
                                        }
                                        catch(e){
                                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('${e}')));
                                          print('Erreur lors de la modification du rendez-vous : ${e}');
                                        }









                                      }, child: Text('Modifier'))




                                    ],)
                              );
                            });



                          },
                        )
                      ],
                    ),
                  ),
                );
              },
            );
          } else {
            return Center(child: Text('No data found.'));
          }
        },
      ),
    );
  }

  Future<List<dynamic>> fetchAppointments(BuildContext context, String username) async {
    final response = await http.post(
      Uri.parse('http://192.168.43.128:5002/rdv'),
      body: json.encode({'username': username}),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 405) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("$username doesn't have any appointment yet")),
      );
      return [];
    } else if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['appointments'];
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: ${response.statusCode}")),
      );
      throw Exception('Failed to load appointments');
    }
  }
}
