import { Text, View, ScrollView } from 'react-native';
import {useState, useEffect} from 'react';
import styles from '../../assets/my_styles';

type Joke = {
  id: number;
  text: string;
  contributer: string; 
  timestamp: string;
};

export default function JokesListScreen() {
  const [jokes, setJokes] = useState<Joke[]>([]);
  const fetchData = async () => {
    const response = await fetch(`https://cs-webapps.bu.edu/ksolter/dadjokes/api/jokes/`);
    const data = await response.json();
    setJokes(data.results);
  }

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <ScrollView>
      <View style={styles.mediumContainer}>
        <View style={styles.titleContainer}>
          <Text style={styles.titleText}>Jokes List</Text>
        </View>
        {jokes.map((joke) => (
          <View key={joke.id} style={styles.smallContainer}>
            <Text style={styles.paragraphText}>{joke.text}</Text>
            <Text style={styles.paragraphText}>Contributed by: {joke.contributer}</Text>
            <Text style={styles.paragraphText}>Timestamp: {joke.timestamp}</Text>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}
