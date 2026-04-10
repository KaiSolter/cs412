import { useState, useEffect } from 'react';
import styles from '../../assets/my_styles';
import { Text, View, ScrollView, Image } from 'react-native';
import { useAuth } from '@/context/AuthContext';

const SITE_BASE_URL = 'https://cs-webapps.bu.edu';
const API_BASE_URL = 'https://cs-webapps.bu.edu/ksolter/mini_insta/api';

type Post = {
  id: number;
  profile_pk: number;
  caption: string;
  timestamp: string;
};

type Photos = {
  id: number;
  image_url?: string | null;
  image_file?: string | null;
  timestamp: string;
};

//method to deal with image_file vs image_url
const resolvePhotoUri = (photo: Photos): string | null => {
  const candidate = photo.image_file || photo.image_url;
  if (!candidate) {
    return null;
  }

  if (candidate.startsWith('http://') || candidate.startsWith('https://')) {
    return candidate;
  }

  if (candidate.startsWith('/')) {
    return `${SITE_BASE_URL}${candidate}`;
  }

  return `${SITE_BASE_URL}/${candidate}`;
};

export default function Feed() {
  const { token, profileId } = useAuth();

  const getAuthHeaders = (): Record<string, string> => {
    if (!token) {
      return {};
    }

    return {
      Authorization: `Token ${token}`,
    };
  };

  const [feed, setFeed] = useState<Post[]>([]);
  const fetchFeed = async (url: string) =>{
    const response = await fetch(url, {
      headers: getAuthHeaders(),
    });
    const data = await response.json();
    setFeed(data.results);
  }

  //store photos keyed by post so we can display them with the post (without having to fetch every time)
  const [photosByPostId, setPhotosByPostId] = useState<Record<number, Photos[]>>({});

  //fetch photos for a given post
  const fetchPhotosForPost = async (postId: number): Promise<Photos[]> => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}/photos/`, {
      headers: getAuthHeaders(),
    });
    const data = await response.json();
    return data.results ?? [];
  };

  useEffect(() => {
    if (!profileId) {
      return;
    }

    fetchFeed(`${API_BASE_URL}/profiles/${profileId}/feed/`);
  }, [profileId]);

  useEffect(() => {
    if (feed.length === 0) {
      return;
    }

    let isCancelled = false;

    //fetch photos for all posts in the feed (just calls fetchPhotosForPost for each post and combines results)
    //reliant on feed so if feed changes it will hopefully re-fetch photos for the new feed (and not fetch photos for old posts that are no longer in the feed)
    const fetchAllPhotos = async () => {
      const entries = await Promise.all(
        feed.map(async (post) => {
          const photos = await fetchPhotosForPost(post.id);
          return [post.id, photos] as const;
        })
      );

      if (!isCancelled) {
        setPhotosByPostId(Object.fromEntries(entries));
      }
    };

    fetchAllPhotos();

    return () => {
      isCancelled = true;
    };
  }, [feed]);


  return (
    <ScrollView>
      <View style={styles.mediumContainer}>
        <View style={styles.titleContainer}>
          <Text style={styles.titleText}>Feed</Text>
        </View>
        <View style={styles.mediumContainer}>
          {feed.map((post) => (
              <View key={post.id} style={styles.smallContainer}>
                <Text style={styles.paragraphText}>{post.caption}</Text>
                <Text style={styles.paragraphText}>Contributed by: {post.profile_pk}</Text>
                <Text style={styles.paragraphText}>Timestamp: {post.timestamp}</Text>
                {(photosByPostId[post.id] ?? []).map((photo) => {
                  const uri = resolvePhotoUri(photo);
                  if (!uri) {
                    return null;
                  }

                  return (
                    <Image
                      key={photo.id}
                      source={{ uri }}
                      style={styles.image}
                      resizeMode="cover"
                    />
                  );
                })}
              </View>
            ))}
          </View>
      </View>
    </ScrollView>
  );
};
