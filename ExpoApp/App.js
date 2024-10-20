import React, { useState, useEffect } from 'react';
import { StyleSheet, TextInput, View, Text, Button, Keyboard, TouchableWithoutFeedback, Alert, Image } from 'react-native';

const App = () => {
  const [risk, setRisk] = useState(null);
  const [description, setDescription] = useState('');
  const [popup, setPopup] = useState(false);

  useEffect(() => {
    submit("")
  }, []);

  return (
      <View style={styles.container}>
        <Text style={styles.label}>Incident Report:</Text>
        <TextInput
          style={styles.input}
          multiline={true}
          numberOfLines={4} 
          placeholder="Type your description here..."
          value={description}
          onChangeText={setDescription} 
        />
        <Button 
          title="Submit" 
          color='rgb(194, 40, 35)'
          onPress={async () => {
            Keyboard.dismiss();
            submit(description).then(res => {
              setRisk(res);
              // setDescription('');
              setPopup(true);
            }).catch(err => {
              Alert.alert('Network error', 'Please check your connection and try again.');
            });
          }} 
        />
        <View style={{height: 100}}>
          {risk && 
            <Text style={styles.preview}>
              Our model predicts that this is a {risk} risk incident.
            </Text>
          }
        </View>
        <View style={{height: 100}}>
          {popup && 
            <View style={{flexDirection: 'row', justifyContent: 'center', gap: 30}} >
              <Button color='rgb(194, 40, 35)' onPress={async () => {
                setPopup(false);
                Alert.alert('Feedback submitted', 'Thanks for helping us improve our model.');
                setRisk(false);
              }} title="Agree" />
              <Button color='rgb(194, 40, 35)' onPress={async () => {
                setPopup(false);
                Alert.alert('Feedback submitted', 'Thanks for helping us improve our model.');
                setRisk(false);
              }} title="Disagree" />
            </View>
          }
        </View>
        <View style={{ justifyContent: 'center', alignItems: 'center' }} >
          <Image style={{maxWidth: 200, alignItems: 'center', marginTop: 150}} source={require("./assets/logo.png")} resizeMode='contain'/>
        </View>
      </View>
  );
};

const submit = async (description) => {
  console.log('Submitting:', description);
  const response = await fetch('http://172.20.10.13:5000/get_risk', {
    method: 'POST', 
    headers: {'content-type': 'application/json'}, 
    body: JSON.stringify({ description }) 
  });

  if (!response.ok) {
    console.error('Network response was not ok');
    throw new Error('Network response was not ok');
  }

  const data = await response.json();
  console.log('Received:', data);

  return data.risk;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    marginTop: 100
  },
  label: {
    fontSize: 18,
    marginBottom: 10,
  },
  input: {
    height: 100,
    borderColor: 'gray',
    borderWidth: 1,
    borderRadius: 5,
    padding: 10,
    marginBottom: 20,
  },
  preview: {
    marginTop: 20,
    fontSize: 20,
  },
});

export default App;
