import 'package:flutter/material.dart';
import 'package:geocoding/geocoding.dart';
import 'package:geolocator/geolocator.dart';
import 'package:myapp/userInterfaces/UserLoginAndSubscription/Doctor.dart';
import 'package:myapp/userInterfaces/UserLoginAndSubscription/DocList.dart';
import 'package:myapp/userInterfaces/SearchDoctorService.dart';

class TheApp extends StatefulWidget {
  final String username;

  TheApp({required this.username});

  @override
  _TheAppState createState() => _TheAppState();
}

class _TheAppState extends State<TheApp> {
  String searchQuery = "";
  Placemark? currentPlace;

  // Get current location permission & coordinates
  Future<Placemark?> getCurrentPlace() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Location services are disabled.")),
      );
      return null;
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied ||
        permission == LocationPermission.deniedForever) {
      permission = await Geolocator.requestPermission();
      if (permission != LocationPermission.whileInUse &&
          permission != LocationPermission.always) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Location permission denied.")),
        );
        return null;
      }
    }

    Position position = await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.high,
    );
    List<Placemark> placemarks =
    await placemarkFromCoordinates(position.latitude, position.longitude);

    return placemarks.isNotEmpty ? placemarks.first : null;
  }

  Future<List<Doctor>> doctorFuture() async {
    if (currentPlace == null) {
      return [];
    }
    // Compose address string from placemark for query parameter
    final address =
        "${currentPlace!.locality}, ${currentPlace!.administrativeArea}, ${currentPlace!.country}";
    if (searchQuery.trim().isEmpty) {
      return await DoctorService.fetchDoctors(address);
    } else {
      return await SearchDoctorService.fetchDoctors(address, searchQuery);
    }
  }

  @override
  void initState() {
    super.initState();

    Future.delayed(Duration.zero, () {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Welcome back ${widget.username}")),
      );
    });

    // Load the current place once on init
    getCurrentPlace().then((place) {
      setState(() {
        currentPlace = place;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    final args = ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>?;
    final username = args?['username'] ?? widget.username;

    return Scaffold(
      appBar: AppBar(
        title: Text("UserSpace"),
        leading: IconButton(
          icon: Icon(Icons.home),
          onPressed: () {
            Navigator.pushNamed(context, '/UserIdentification');
          },
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.menu),
            onPressed: () {
              showMenu(
                context: context,
                position: RelativeRect.fromLTRB(1000, 80, 0, 0),
                items: [
                  PopupMenuItem(
                    child: TextButton(
                      onPressed: () {
                        showDialog(
                          context: context,
                          builder: (BuildContext context) {
                            return AlertDialog(
                              title: Text('About me'),
                              content: SingleChildScrollView(
                                child: Text(
                                  'This app was built to help users find the nearest doctor they need to see.',
                                  style: TextStyle(fontSize: 16),
                                ),
                              ),
                              actions: [
                                TextButton(
                                  onPressed: () => Navigator.pop(context),
                                  child: Text('Close'),
                                ),
                                TextButton(
                                  onPressed: () {
                                    Navigator.pushNamed(context, '/AboutUs');
                                  },
                                  child: Text('More'),
                                ),
                              ],
                            );
                          },
                        );
                      },
                      child: Text('About us'),
                    ),
                  ),
                  PopupMenuItem(
                    child: TextButton(
                      onPressed: () async {
                        Navigator.pop(context); // Close the popup menu
                        Placemark? place = await getCurrentPlace();
                        if (place != null) {
                          // Delay needed to allow the menu to fully close before using the context
                          await Future.delayed(Duration(milliseconds: 100));
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(
                                "You are in: ${place.name}, ${place.locality}, ${place.country}",
                              ),
                            ),
                          );
                        }
                      },

                      child: Text('View your current Location'),
                    ),
                  ),



                  PopupMenuItem(
                    child: TextButton(
                      onPressed: () {
                        Navigator.pushNamed(context, '/appointment',
                            arguments: {'username': username});
                      },
                      child: Text('My appointments'),
                    ),
                  ),
                ],
              );
            },
          ),
        ],
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              decoration: InputDecoration(
                hintText: "Type your search...",
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.search),
              ),
              onSubmitted: (input) {
                setState(() {
                  searchQuery = input;
                });
              },
            ),
            SizedBox(height: 16),
            Expanded(
              child: currentPlace == null
                  ? Center(child: CircularProgressIndicator())
                  : FutureBuilder<List<Doctor>>(
                future: doctorFuture(),
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return Center(child: CircularProgressIndicator());
                  } else if (snapshot.hasError) {
                    return Center(child: Text('Error: ${snapshot.error}'));
                  } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                    return Center(child: Text('No doctors found.'));
                  }

                  final doctors = snapshot.data!;
                  return ListView.builder(
                    itemCount: doctors.length,
                    itemBuilder: (context, index) {
                      final doctor = doctors[index];
                      return Card(
                        margin: EdgeInsets.all(10),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: InkWell(
                          onTap: () {
                            Navigator.pushNamed(
                              context,
                              '/add_rdv',
                              arguments: {
                                'nomDoc': doctor.name,
                                'prenomDoc': doctor.prenom,
                               'Mail' : username
                              },
                            );
                          },
                          child: ListTile(
                            leading: Icon(Icons.local_hospital, color: Colors.blue),
                            title: Text(
                              doctor.name + ' ' + doctor.prenom,

                              style: TextStyle(fontWeight: FontWeight.bold),
                            ),
                            subtitle: Text('${doctor.speciality} • ${doctor.location}'),
                          ),
                        ),


                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
