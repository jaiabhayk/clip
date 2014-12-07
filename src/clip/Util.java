/**
 * 
 */
package clip;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

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

		String info = removeDuplicates(train, test, destTrain, destTest);
		File file1 = new File(infoFile);
		FileWriter fileWriter = new FileWriter(file1);
		fileWriter.write(info);
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
