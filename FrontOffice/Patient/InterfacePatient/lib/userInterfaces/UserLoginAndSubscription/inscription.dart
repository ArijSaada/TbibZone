import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter/material.dart';
import 'connexion.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


/*class InscriptionPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Inscription"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          child<Widget>ren: <Widget>[
            // Email input field
            TextField(
              decoration: InputDecoration(
                labelText: 'Email',
                hintText: 'Enter your email',
              ),
            ),

            // Password input field
            TextField(
              obscureText: true,
              decoration: InputDecoration(
                labelText: 'Password',
                hintText: 'Enter your password',
              ),
            ),

            // Add button
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 16.0),
          child: Column(
            children: [
              ElevatedButton(
                onPressed: () {
                  // 
                },
                child: Text('Add'),
              ),
              ElevatedButton(
                onPressed: () {
                  // 
                },
                child: Icon(Icons.chat_outlined),
              ),
            ],
          ),
        ),

    ),
          ],
        ),
      ),
    );
  }
}*/


class InscriptionPage extends StatefulWidget {
  @override
  _Inscription createState() => _Inscription();
}
class _Inscription extends State<InscriptionPage> {
  String usermail = '';
  String username = '';
  String prenom = '';
  String userpwd = '';
  bool accountExists = false;
  List missing = [];
  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        title: Text("Inscription"),
        leading: IconButton(onPressed:() {
          Navigator.pushNamed(context, '/UserIdentification');
        }, icon: Icon(Icons.home)),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            TextField(
              decoration: InputDecoration(
                labelText: 'Nom',
                hintText: 'Enter your name',
              ),
              onChanged: (value) {username = value;},
            ),
            TextField(
              decoration: InputDecoration(
                labelText: 'Prenom',
                hintText: 'Enter your prenom',
              ),
              onChanged: (value) {prenom = value;},
            ),
            // Email input field
            TextField(
              decoration: InputDecoration(
                labelText: 'Email',
                hintText: 'Enter your email',

              ),

              onChanged: (value) {usermail = value;},
            ),


            // Password input field
            TextField(
              //obscureText: true,
              decoration: InputDecoration(
                labelText: 'Password',
                hintText: 'Enter your password',

              ),
              onChanged: (value) {userpwd = value ;},
            ),

            // Padding and button column
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 16.0),
              child: Column(
                children: [
                  ElevatedButton(

                    onPressed: () async{setState(() {
            missing.clear();
            });


            if (usermail.isEmpty) {
            missing.add("Email");
            }
            if (userpwd.isEmpty) {
            missing.add("Password");
            }
            if (missing.isNotEmpty) {
            ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(
            "${missing.join(',') } is/are missing")));
            return;
            }

            else {
            try {

            final response = await http.post(
            Uri.parse('http://192.168.1.19:5001/add_patient'),
            headers: {'Content-Type': 'application/json'},
            body: json.encode(
            {'email': usermail, 'password': userpwd,'nom' : username, 'prenom' : prenom}),
            );





            ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text ('Status : ${response.statusCode}')));
            ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Body : ${response.body}')));





            if (response.statusCode == 400) {
              setState(() {
            accountExists = true;

            });}
            else {
              if (response.statusCode == 201) {
                //ya3ni user created tawa
                Navigator.pushNamed(
                    context, '/using', arguments: {'username': usermail});
              }
              else {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text(
                      "Unexpected error: ${response.statusCode}")),
                );
              }
            }
            if (accountExists) {
            showDialog(
            context: context,
            builder: (BuildContext context) {
            return AlertDialog(
            title: Text('Account Exists'),
            content: Text("You already have an account."),
            actions: [
            TextButton(
            onPressed: () {
            Navigator.pushNamed(context, '/connexion');
            },
            child: Text('Go to Login'),
            ),
            TextButton(
            onPressed: () {
            Navigator.pop(context);  // Close the dialog
            },
            child: Text('Cancel'),
            ),
            ],
            );
            },
            );
            }





            if (accountExists) {
    showDialog(
    context: context,
    builder: (BuildContext context) {
    return AlertDialog(
    title: Text('Account Exists'),
    content: Text("You already have an account."),
    actions: [
    TextButton(
    onPressed: () {
    Navigator.pushNamed(context, '/connexion');
    },
    child: Text('Go to Login'),
    ),
    TextButton(
    onPressed: () {
    Navigator.pop(context); // Close the dialog
    },
    child: Text('Cancel'),
    ),
    ],
    );
    },
    );
    }
    }


            

            catch (e) {
            print('An error occurred: $e');
            }



            }
            },








                      //

                    child: Text('Add'),
                  ),

                  /*if (accountExists)
                    Container(
                      padding: EdgeInsets.all(10.0),
                      decoration: BoxDecoration(

                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      child: ElevatedButton(
                          onPressed: () {
                            Navigator.pushNamed(
                                context, "/connexion"

                            );
                            // 
                          },
                          child: Text("You already have an account . ")
                      ),


                    ),

                   */





    ElevatedButton(
                    onPressed: () async {
                      print("Button pressed!");

                      Navigator.pushNamed(context, "/chat", arguments: {'username',usermail});
                    },

                    child: Icon(Icons.chat_outlined),
                  ),

                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
