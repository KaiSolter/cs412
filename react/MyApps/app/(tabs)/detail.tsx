// react/MyApps/app/(tabs)/detail.tsx 
// Author: Kai Solter
// This is a scrollable screen which displays interspersed images and text
import { View, Text, Image, ScrollView } from 'react-native';
import styles from '@/assets/my_styles';


export default function DetailScreen() {
  return (
    <ScrollView> 
      <Text style={styles.titleText}>Chainsawman (Yoru) Details</Text>
      <Text style={styles.paragraphText}>Chainsawman By Tatsuki Fujimoto is a manga series which is published by the Japanese entertainment conglomerate Shueisha. 
         Chainsawman was a smash hit, quickly gaining popularity due to the creative art style and non standard storytelling techniques.
         In particular many of the main characters do things that are morally questionable and the manga portrays many tragic events through the 
         lens of black comedy or absurdism. The story is also full of twists and subseversions, making for a compelling and unpredictable read. 
         My favorite part of the story is its ability to balance dark themes and black humor with deep thematic ideas.</Text>
      <Image
        source={{ uri: 'https://cs-people.bu.edu/ksolter/images/csm1.png' }}
        style={styles.image}
        resizeMode="contain"
      />
      <Text style={styles.subTitleText}>The above is the main villian of chainsawman part 2, Yoru, who is possessing Asa Mitaka</Text>
      <Image
        source={{ uri: 'https://cs-people.bu.edu/ksolter/images/csm2.png' }}
        style={styles.image}
        resizeMode="contain"
      />
      <Text style={styles.subTitleText}>This is Yoru, declaring her motivations</Text>
      <Image
        source={{ uri: 'https://cs-people.bu.edu/ksolter/images/csm3.png' }}
        style={styles.image}
        resizeMode="contain"
      />
      <Text style={styles.subTitleText}>Yoru after she possessed Asa</Text>
    </ScrollView>
  
  );
}

