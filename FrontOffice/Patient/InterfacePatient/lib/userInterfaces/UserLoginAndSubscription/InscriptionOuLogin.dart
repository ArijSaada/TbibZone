import 'package:flutter/material.dart';
import 'connexion.dart';
import 'inscription.dart';
/*class account extends statelessWidget {
  return Scaffold (
  AppBar: appbar(

  )
  )
  Body : Column (
  child :
      Row : (
  children : [
  FLoatingActionButton (
  onPressed () { Navigator.push(inscription)}



  child : Icon (Icons.add)
  );
  FLoatingActionButton (
  onPressed () { Navigator.push(connexion)}



  child : Icon (Icons.Login)
  ]
  )

  )

  )
} */


class Account extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("User world"),
      ),
      body: Center(
        child: Column(


          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
        Center(
        child: Row(
              mainAxisAlignment: MainAxisAlignment.center,

              children: [
                FloatingActionButton(
                  onPressed: () {
                    Navigator.pushNamed(context, "/inscription");
                  },
                  child: Icon(Icons.add),
                ),
                SizedBox(width: 20), // Adds spacing between buttons
                FloatingActionButton(
                  onPressed: () {
                    Navigator.pushNamed(context, "/connexion");
                  },
                  child: Icon(Icons.login),
                ),
                SizedBox(width: 20),
                FloatingActionButton(
                  onPressed: () async {
                    print("Button pressed!");

                    Navigator.pushNamed(context, "/chat");
                  },

                  child: Icon(Icons.chat_outlined),
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
