import { Text, View, Image } from 'react-native';
import {useState, useEffect} from 'react';
import styles from '../../assets/my_styles';

export default function IndexScreen() {

  const [joke, setJoke] = useState<{ text: string; contributer?: string }>({ text: '' });
  const [image, setImage] = useState<{ image_url: string }>({ image_url: '' });

  const fetchData = async (url: string, joke : boolean) =>{
    const response = await fetch(url);
    const data = await response.json();
    if (joke) {
      setJoke(data);
    } else {
      setImage(data);
    }
  }
  useEffect(() => {
    fetchData(`https://cs-webapps.bu.edu/ksolter/dadjokes/api/random/`, true);
  }, []);
  useEffect(() => {
    fetchData(`https://cs-webapps.bu.edu/ksolter/dadjokes/api/random_picture/`, false);
  }, []);

  return (
    <View style={styles.mediumContainer}>
      <View style={styles.smallContainer}>
        <View style={styles.titleContainer}>
          <Text style={styles.titleText}>Random Joke</Text>
        </View>
        <Text style={styles.subTitleText}>Here's a random joke by {joke.contributer}:</Text>
        <Text style={styles.paragraphText}>{joke.text}</Text>
      </View>
      <Image style={styles.image} source={{ uri: image.image_url }} />
    </View>
  );
}
