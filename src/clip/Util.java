/**
 * 
 */
package clip;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

/**
 * @author JaiAbhay
 *
 */
public class Util {

	private static final String NEW_ENTRY_SEPARATOR = "===========================================================================\n";

	/**
	 * @param args
	 * @throws Exception
	 */
	public static void main(String[] args) throws Exception {
		
		String pathPrefix = "DataCopy1";
		String train = pathPrefix + "/" + "TrainingSet.txt";
		String test = pathPrefix + "/" + "TrialSet.txt";
		;
		String destTrain = pathPrefix + "/" + "TrainingSetCleaned.txt";
		String destTest = pathPrefix + "/" + "TrialSetCleaned.txt";
		String infoFile = pathPrefix + "/" + "cleaningInfoFile.txt";

/*		String info = removeDuplicates(train, test, destTrain, destTest);
		File file1 = new File(infoFile);
		FileWriter fileWriter = new FileWriter(file1);
		fileWriter.write(info);
		fileWriter.flush();
		fileWriter.close();*/
		
		convdertAndWriteForPosTagger(destTrain);
		convdertAndWriteForPosTagger(destTest);
		
	}
    
	//Writes in a format which pos tagger can understand
	//output file name is fileName.posTagger.tmp
	private static void convdertAndWriteForPosTagger(String source) throws Exception {
		String destFile = source +".posTagger.tmp";
		File file = new File(source);
		FileReader fileReader = new FileReader(file);
		StringBuilder sb = new StringBuilder();
		BufferedReader bufferedReader = new BufferedReader(fileReader);
		String line;
		try {
			while ((line = bufferedReader.readLine()) != null) {
				Tweet tweet = new Tweet(line);
				sb.append(tweet.getTweet() +"\n");
			}
		} finally {
			fileReader.close();
		}
		
		File file1 = new File(destFile);
		FileWriter fileWriter = new FileWriter(file1);
			fileWriter.write(sb.toString());
		fileWriter.flush();
		fileWriter.close();
		
		
		
	}

	private static String removeDuplicates(String source1, String source2,
			String dest1, String dest2) throws Exception {
		File file = new File(source1);
		FileReader fileReader = new FileReader(file);
		BufferedReader bufferedReader = new BufferedReader(fileReader);
		String line;
		Map<String, Tweet> trainTweets = new HashMap<String, Tweet>();
		try {
			while ((line = bufferedReader.readLine()) != null) {
				Tweet tweet = new Tweet(line);
				trainTweets.put(tweet.getOldId(), tweet);
			}
		} finally {
			fileReader.close();
		}

		file = new File(source2);
		fileReader = new FileReader(file);
		bufferedReader = new BufferedReader(fileReader);
		Map<String, Tweet> testTweets = new HashMap<String, Tweet>();
		StringBuilder sb = new StringBuilder();
		int duplicates = 0;
		int scoreMismatch = 0;
		try {
			while ((line = bufferedReader.readLine()) != null) {
				Tweet testTweet = new Tweet(line);

				if (trainTweets.containsKey(testTweet.getOldId())) {
					Tweet trainTweet = trainTweets.get(testTweet.getOldId());
					sb.append(NEW_ENTRY_SEPARATOR);
					sb.append("Duplicate entry found in the training set:-\n");
					sb.append("trainTweet:- " + trainTweet + "\n");
					sb.append("testTweet:- " + testTweet + "\n");

					duplicates++;

					Tweet t = Tweet.mergeTweets(trainTweet, testTweet);
					if ((trainTweet.getOldScore() - testTweet.getOldScore()) > 0.2 
							|| (trainTweet.getOldScore() - testTweet.getOldScore()) < -0.2) {
						sb.append("Score mismatch between testTweet and trainTweet:- "
								+ testTweet.getOldScore()
								+ "/"
								+ trainTweet.getOldScore() + "\n");
						scoreMismatch++;
						
					} else {
					sb.append("Merged trainTweet:- \n" + t + "\n");
					sb.append(NEW_ENTRY_SEPARATOR);
					testTweets.put(t.getOldId(), t);
					}
					trainTweets.remove(testTweet.getOldId());
				} else {
					testTweets.put(testTweet.getOldId(), testTweet);
				}

			}
		} finally {
			fileReader.close();
		}
		
		Random randomGenerator = new Random();
		HashSet s = new HashSet<Integer>();
	    while (true) {
	      int randomInt = randomGenerator.nextInt(trainTweets.size()+1);
	      s.add(randomInt);
	      if (s.size() == 500) {
	    	  //sb.append("\n intergers:- " + s +"\n");
	    	  break;
	      }
	    }
	    
	    ArrayList<String> keys = new ArrayList<String>();
	    for (String key:trainTweets.keySet()) {
	    	keys.add(key);
	    	
	    }
	   
	    
	    Iterator it = s.iterator() ;
	    
	    while (it.hasNext()) {
	    	String key = keys.get((int) it.next());
	    	Tweet val = trainTweets.remove(key) ;
	    	testTweets.put(key, val);
	    	//sb.append("\n val:-" + val + "\n");
	    	
	    }
	    
		sb.append("no of duplicates found:- " + duplicates + "\n");
		sb.append("no of duplicates with score mismatch found:- "
				+ scoreMismatch + "\n");
		sb.append("Train data size:- " + trainTweets.size() + "\n");
		sb.append("Test data size:- " + testTweets.size() + "\n");
		System.out.println(sb);

		writeTweetsToFile(dest1, trainTweets);
		writeTweetsToFile(dest2, testTweets);

		return sb.toString();
	}

	/**
	 * @param dest1
	 * @param trainTweets
	 * @throws IOException
	 */
	private static void writeTweetsToFile(String dest1,
			Map<String, Tweet> trainTweets) throws IOException {
		File file1 = new File(dest1);
		FileWriter fileWriter = new FileWriter(file1);
		for (Tweet t : trainTweets.values()) {
			fileWriter.write(t.toString());
			fileWriter.write("\n");
		}
		fileWriter.flush();
		fileWriter.close();
	}

}
