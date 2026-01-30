import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class AboutUsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('About Us'),
        backgroundColor: Colors.green,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Introduction Section
              Text(
                'Welcome to Tbibzone',
                style: TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: Colors.green,
                ),
              ),
              SizedBox(height: 10),
              Text(
                'Our app connects patients with healthcare professionals in a seamless way, '
                    'offering a platform for easy appointment scheduling, medical consultation, and healthcare management.',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.black54,
                ),
              ),
              SizedBox(height: 30),

              // ITSS Overview Section
              Text(
                'Powered by ITSS Global (Information Technology Services and Solutions)',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  color: Colors.green,
                ),
              ),
              SizedBox(height: 10),
              Text(
                'ITSS ensures that our app runs smoothly with innovative technology, providing fast, '
                    'accurate, and personalized responses. Our AI-powered chatbot, InternChat, allows users to easily access this app.',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.black54,
                ),
              ),
              SizedBox(height: 30),

              // Mission & Vision Section
              Text(
                'Mission & Vision',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.green,
                ),
              ),
              SizedBox(height: 10),
              Text(
                'Mission: Insuring that every tourist or visitor can find the all the nearby doctors he needs by just a few clicks.',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.black54,
                ),
              ),
              SizedBox(height: 10),
              Text(
                'Vision: A world where technology and healthcare work together to provide better care for all.',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.black54,
                ),
              ),
    ],
    ),
    )
    ),
    );




  }


}