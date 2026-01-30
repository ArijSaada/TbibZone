class Doctor {
  final String name;
  final String speciality;
  final String location;
  final String prenom;

  Doctor({
    required this.name,
    required this.speciality,
    required this.location,
    required this.prenom
  });

  factory Doctor.fromJson(Map<String, dynamic> json) {
    return Doctor(
      name: json['nomDoc'] ?? 'No name',
      prenom : json['prenom'] ?? 'non prenom',

      speciality: json['speciality'] ?? 'No speciality',
      location: json['location'] ?? 'No location',
    );
  }
}
