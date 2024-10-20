import React, { useState, useEffect } from 'react';
import { StyleSheet, TextInput, View, Text, Button } from 'react-native';

const App = () => {
  const [risk, setRisk] = useState(null);
  const [description, setDescription] = useState('');

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Enter Description of incident:</Text>
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
        onPress={async () => {
          res = await submit(description);
          setRisk(res);
        }} 
      />
      {risk && 
        <Text style={styles.preview}>
          Risk Level: {risk}
        </Text>
      }
    </View>
  );
};

const submit = async (description) => {
  console.log('Submitting:', description);
  const response = await fetch('http://172.27.127.36:5000/get_risk', { 
    method: 'POST', 
    headers: {'content-type': 'application/json'}, 
    body: JSON.stringify({ description }) 
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  console.log('Received:', data);

  const data = await response.json();
  return data.risk;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
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
    fontSize: 16,
  },
});

export default App;
