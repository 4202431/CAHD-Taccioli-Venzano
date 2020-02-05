import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

public class Main {
	public static void main(String[] args) {
		String folder = "C:\\Users\\Gabriele\\Desktop\\CAHD_Ema";
		int qid_size = Integer.parseInt(args[0]);
		int sensitive_size = Integer.parseInt(args[1]);
		double density = Double.parseDouble(args[2]);
		try{
			File f1 = new File(folder+"\\data_transaction.csv");
			File f2 = new File(folder+"\\list_items.txt");
			f2.delete();
			f1.delete();
			BufferedWriter writer;		
			for (int i = 0; i < qid_size; i++){
				writer = new BufferedWriter(new FileWriter(folder+"\\data_transaction.csv", true));
				String textToAppend="";
				for (int j=0; j < qid_size + sensitive_size; j++){
					double temp = Math.random();
					if (temp < density)
						textToAppend += "1";
					else
						textToAppend += "0";
					if (j != qid_size + sensitive_size -1){
						textToAppend += ",";
					}
				}
				if (i!=0)
					writer.newLine(); 
				writer.write(textToAppend);
				writer.close();
			}
			System.out.println("Success");
			for (int i = 0; i < qid_size+sensitive_size; i++){
				writer = new BufferedWriter(new FileWriter(folder+"\\list_items.txt", true));
				String textToAppend=String.valueOf(i);
				if (i!=0)
					writer.newLine(); 
				writer.write(textToAppend);
				writer.close();
			}
			System.out.println("Success");
		}catch(Exception e) {
			System.out.println(e.getMessage());
			e.printStackTrace();
		}
		return;
	} 
}