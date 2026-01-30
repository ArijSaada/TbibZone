import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
class ChatbotInterface extends StatefulWidget {
  @override
  _ChatbotInterfaceState createState() => _ChatbotInterfaceState();
}

class _ChatbotInterfaceState extends State<ChatbotInterface>{

  TextEditingController _controller = TextEditingController();
  String _response = '';
  String postUrl = 'http://192.168.1.19:8000/chat';
  String getUrl = 'http://192.168.1.19:8000/';
String userInput ='';
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title: Text("Chatbot")
      ),
      body: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              TextField(
                controller: _controller,
                decoration: InputDecoration(
                  // Label for text field
                    border: OutlineInputBorder(),
                    hintText: 'Enter your question',

                ),
                onChanged: (value) {userInput = value; },
                onSubmitted: (value) async {
                  //String userInput = _controller.text.trim();
                  if (userInput.isEmpty) {
                    _response = 'Empty question';
                  }
                  else {
                    userInput = userInput.toLowerCase();
                    final response = (await http.post(Uri.parse(postUrl),
                        headers: <String, String>{
                          'Content-Type': 'application/json',
                        },
                        body: jsonEncode(
                            <String, String>{
                              'question': userInput,
                            }
                        )

                    )); //as String;
                    if (response.statusCode == 200) {
                      setState(() {
                        _response = jsonDecode(response.body)['answer'];
                      });
                    }
                    else {
                      setState(() {
                        _response = 'Probleme de POST API: ' +
                            'Error: ${response.statusCode}';
                      });
                      _controller.clear();
                    };
                  };
                }

              ),
              /*ElevatedButton(
                onPressed: () async {
                  String userInput = _controller.text.trim();
                  if (userInput.isEmpty) {
                    _response = 'Empty question';
                  }
                  else {
                    userInput = userInput.toLowerCase();
                    final response = (await http.post(Uri.parse(postUrl),
                        headers: <String, String>{
                          'Content-Type': 'application/json',
                        },
                        body: jsonEncode(
                            <String, String>{
                              'question': userInput,
                            }
                        )

                    )); //as String;
                    if (response.statusCode == 200) {
                      setState(() {
                        _response = jsonDecode(response.body)['answer'];
                      });
                    }
                    else {
                      setState(() {
                        _response = 'Probleme de POST API: ' + 'Error: ${response.statusCode}';

                      });
                      _controller.clear();
                    }
                  }
                },



                child: Text('Submit'),
              ),

               */
              SizedBox(
                  height: 20

              ),
              Text('You :  '+ userInput, style: TextStyle(fontSize: 18)),
              SizedBox(
                  height: 20

              ),
              Text('Answer :  ' + _response, style: TextStyle(fontSize: 18))



            ],
          )

      ),
    );




  }
}




