import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:myapp/userInterfaces/Appointments.dart';
import 'userInterfaces/UserLoginAndSubscription/inscription.dart';
import 'userInterfaces/UserLoginAndSubscription/connexion.dart';
import 'userInterfaces/UserLoginAndSubscription/InscriptionOuLogin.dart';
import 'userInterfaces/PriseRdv.dart';

import 'userInterfaces/AppFunction.dart';
import 'chatbotInterface.dart';
import 'userInterfaces/AboutUs.dart';
import 'userInterfaces/Appointments.dart';

void main() {

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {


  const MyApp({super.key});


  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(

      debugShowCheckedModeBanner : false,
      initialRoute: '/',
      routes: {
        '/appointment': (context){
        final args = ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>;
        final username = args?['username'];
        return AppointmentsScreen(username: username ?? '');
        },
        '/add_rdv': (context){
          final args = ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>;
          final nomDoc = args?['nomDoc'];
          final userEmail = args?['Mail'];
          final prenomDoc = args?['prenomDoc'];
          return AppointmentPage( nomDoc: nomDoc, prenomDoc: prenomDoc, userEmail: userEmail,);
        },

        '/AboutUs' : (context) => AboutUsPage(),
        '/chat': (context) => ChatbotInterface(),
        '/inscription': (context) => InscriptionPage(),
        '/connexion': (context) => LoginState(),

        '/UserIdentification': (context) => Account(),


        '/using': (context) {
          final args = ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>;
          final username = args?['username'];
          return TheApp(username: username ?? '');
        },
      },
      title: 'Flutter Demo',

    theme: ThemeData(
        // This is the theme of your application.
        //
        // TRY THIS: Try running your application with "flutter run". You'll see
        // the application has a purple toolbar. Then, without quitting the app,
        // try changing the seedColor in the colorScheme below to Colors.green
        // and then invoke "hot reload" (save your changes or press the "hot
        // reload" button in a Flutter-supported IDE, or press "r" if you used
        // the command line to start the app).
        //
        // Notice that the counter didn't reset back to zero; the application
        // state is not lost during the reload. To reset the state, use hot
        // restart instead.
        //
        // This works for code too, not just values: Most code changes can be
        // tested with just a hot reload.
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Tbibzone'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // TRY THIS: Try changing the color here to a specific color (to
        // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
        // change color while the other colors stay the same.
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Center(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  FloatingActionButton(
                    onPressed: () {
                      Navigator.pushNamed(context, "/UserIdentification");
                    },
                    child: Icon(Icons.person_3),
                  ),


                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
