import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'connexion.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';



class LoginState extends StatefulWidget {
  @override
  _Login createState() => _Login();
}
class _Login extends State<LoginState> {
  String usermail = '';
  String userpwd = '';
  bool boolPass = true;
  bool accountExists = true;
  List missing = [];
  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        title: Text("Login"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
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
              obscureText: true,


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
                          Uri.parse('http://192.168.43.128:5000/login'),
                          headers: {'Content-Type': 'application/json'},
                          body: json.encode(
                              {'mail': usermail, 'pwd': userpwd}),
                        );





                        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text ('Status : ${response.statusCode}')));
                        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(' ${response.body}')));





                        if (response.statusCode == 404) {
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('User not found')));

                          setState(() {

                            accountExists = false;

                          });}
                        else {
                          if (response.statusCode == 200) {
                            Navigator.pushNamed(
                                context, '/using', arguments: {'username': usermail});
                          }
                          else {
                            if (response.statusCode == 402) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(content: Text('wrong password')));
                              setState(() {
                                boolPass = false;
                              });

                            }
                            else {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text(
                                    "Unexpected error: ${response
                                        .statusCode}")),
                              );
                            }
                          }
                        }






                      }

                      catch (e) {
                        print('An error occurred: $e');
                      }



                    }
                    },








                    //

                    child: Text('Login'),
                  ),

                  if (accountExists == false || missing.contains('Email'))

                     Container(
                      padding: EdgeInsets.all(42.0),
                      decoration: BoxDecoration(

                        borderRadius: BorderRadius.circular(42.0),
                      ),
                         child: Column(
                           mainAxisAlignment: MainAxisAlignment.center,  // Center the buttons vertically
                           children: [
                           Row(
                           mainAxisAlignment: MainAxisAlignment.center,  // Center the buttons horizontally
                           children: [
                          ElevatedButton(
                              onPressed: () {
                                Navigator.pushNamed(
                                    context, "/inscription"

                                );

                                //
                              },
                              child: Icon(Icons.add)
                          ),

                           SizedBox(),
                           ],
                         )
                         ]
                         )
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
