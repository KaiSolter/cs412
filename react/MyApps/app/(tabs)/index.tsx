// react/MyApps/app/(tabs)/index.tsx 
// Author: Kai Solter
// This is the index screen for the tabs navigator, it displays some text and an image
import { Text, View, Image } from 'react-native';
import styles from '@/assets/my_styles';
const cover = require('@/assets/images/csmcover.png');

export default function IndexScreen() {
  return (
    <View>
      <View style={styles.textContainer}>
        <Text style={styles.titleText}>Chainsawman info</Text>
        <Text style={styles.subTitleText}>Information about the manga and anime series Chainsawman</Text>
      </View>
      <Image source={cover} style={styles.image} />
    </View>
  );
}