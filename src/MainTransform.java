import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.io.*;  
import java.util.Scanner;  

public class MainTransform {
	public static void main(String[] args) {
		try{
			File file=new File("transactional_T10I4D1000K.csv");    //creates a new file instance  
			FileReader fr=new FileReader(file);   //reads the file  
			BufferedReader br=new BufferedReader(fr);  //creates a buffering character input stream  
			ArrayList<String> rows = new ArrayList<>();
			String line;  
			while((line=br.readLine())!=null)  {  
				rows.add(line);
			}  
			fr.close();    //closes the stream and release the resources  
			ArrayList<String> sensitive = new ArrayList<>();
			for (int i = 0; i < rows.size(); i++){
				String[] each = rows.get(i).split(",");
				for (int j=0; j < each.length; j++) {
					if (!sensitive.contains(each[j])) {
						sensitive.add(each[j]);
					}
				}
			}
			System.out.println("Rows size : "+rows.size());
			System.out.println("Columns size : "+sensitive.size());
			File f1 = new File("data_transaction.csv");
			File f2 = new File("list_items.txt");
			f2.delete();
			f1.delete();
			BufferedWriter writer;		
			for (int i = 0; i < sensitive.size(); i++){
				writer = new BufferedWriter(new FileWriter("list_items.txt", true));
				String textToAppend=sensitive.get(i);
				if (i!=0)
					writer.newLine(); 
				writer.write(textToAppend);
				writer.close();
			}
			System.out.println("Success");
			for (int i = 0; i < rows.size(); i++){
				System.out.println("Riga : "+i);
				writer = new BufferedWriter(new FileWriter("data_transaction.csv", true));
				String textToAppend="";
				String[] each = rows.get(i).split(",");
				ArrayList<String> this_row = new ArrayList<>();
				for (int j=0; j < each.length; j++) {
					this_row.add(each[j]);
				}
				System.out.println("Densità : "+this_row.size());
				for (int j=0; j < sensitive.size(); j++){
					if (this_row.contains(sensitive.get(j)))
						textToAppend += "1";
					else
						textToAppend += "0";
					if (j < sensitive.size()-1){
						textToAppend += ",";
					}
				}
				if (i!=0)
					writer.newLine(); 
				writer.write(textToAppend);
				writer.close();
			}
			System.out.println("Success");
		} catch (Exception e){
			System.out.print(e.getMessage());
		}
	} 
}