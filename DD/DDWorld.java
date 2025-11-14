import java.util.Random;
public class DDWorld {
    public String[][] world;
    int playerRow, playerCol = 0;
    boolean rope = true;
    boolean arrow;
    boolean dragonKilled = false;
    String previousMove;
    public DDWorld(){
        world = new String[10][10];
        for (int i = 0; i < 10; i++){
            for (int j = 0; j < 10; j++){
                world[i][j] = " ";
            }
        }
    }
    
    public boolean checkSurroundings(int row,int column){
        int up = row-1;
        int down = row + 1;
        int left = column - 1;
        int right = column + 1;

        if (up < 0){
            up = 9;
        }
        if (down > 9){
            down = 0;
        } 
        if (left < 0){
            left = 9;
        }
        if (right > 9){
            right = 0;
        }

        if ((world[up][column] == "X") & (world[down][column] == "X") & (world[row][left] == "X") & (world[row][right] == "X")) {
            return true;
        } else{
            return false;
        }

    }

    public void clearCharacter(String character) {
        for(int i = 0; i < 10; i++){
            for(int j = 0; j < 10; j++){
                if(world[i][j] == character) {
                    world[i][j] = " ";
                } 
            }
        }
    }

    public void spawnRope() {
        int randRow;
        int randColumn;
        boolean ropeSpawn;
        Random rand = new Random();
        do {
            randRow = rand.nextInt(10);
            randColumn = rand.nextInt(10);
            if (checkSurroundings(randRow, randColumn) == false && (world[randRow][randColumn] == " ")){
                world[randRow][randColumn] = "--"; 
                ropeSpawn = true;
            } else {
                ropeSpawn = false;
                clearCharacter("--");
            }
        } while (ropeSpawn == false);
    }

    public void spawnArrow() {
        int randRow;
        int randColumn;
        boolean arrowSpawn;
        Random rand = new Random();
        do {
            randRow = rand.nextInt(10);
            randColumn = rand.nextInt(10);
            if (checkSurroundings(randRow, randColumn) == false && (world[randRow][randColumn] == " ")){
                world[randRow][randColumn] = "->"; 
                arrowSpawn = true;
            } else {
                arrowSpawn = false;
                clearCharacter("->");
            }
        } while (arrowSpawn == false);
    }

    public String notification(int row, int col) {
        String notification = "There is ";
        boolean nothing = true;
        int pits = 0;

        int up = row-1;
        int down = row + 1;
        int left = col - 1;
        int right = col + 1;
        if (up < 0){
            up = 9;
        }
        if (down > 9){
            down = 0;
        } 
        if (left < 0){
            left = 9;
        }
        if (right > 9){
            right = 0;
        }

        //checks adjacent boxes and notifies what object 
        if (world[up][col].trim().equals("%") || world[down][col].trim().equals("%") || world[row][left].trim().equals("%") || world[row][right].trim().equals("%")){
            notification+="dragon, ";
            nothing = false;
        }
        if (world[up][col].trim().equals("--") || world[down][col].trim().equals("--") || world[row][left].trim().equals("--") || world[row][right].trim().equals("--")) {
            notification+="rope, ";
            nothing = false;
        } 
        if (world[up][col].trim().equals("->") || world[down][col].trim().equals("->") || world[row][left].trim().equals("->") || world[row][right].trim().equals("->")) {
            notification+="arrow, ";
            nothing = false;
        } 
        if (world[up][col].trim().equals("X")){
            pits++;
            nothing = false;
        }
        if (world[down][col].trim().equals("X")){
            pits++;
            nothing = false;
        }
        if (world[row][left].trim().equals("X")){
            pits++;
            nothing = false;
        }
        if (world[row][right].trim().equals("X")){
            pits++;
            nothing = false;
        }

        if (pits == 1){
            notification+="pit, ";
        } else if(pits >= 1){
            notification = notification.substring(0, notification.length() - 3);
            notification+= "are " + pits + " pits, ";
        }


        if (nothing == true){
            notification = "Notification: ";
            return notification;
        } else{
            notification = notification.trim();
            notification = notification.substring(0, notification.length() - 1);
            notification += " in an adjacent room";
            return notification;
        }
    }

    public boolean checkDead(int row, int col){
        
        if (world[row][col].trim().equals("XO")){
            if (rope == true){
                rope = false;
                world[row][col] = " X";
                
                switch (previousMove){
                    case "Left":
                    playerCol++;
                    if (playerCol > 9){
                        playerCol = 0;
                    }
                    world[playerRow][playerCol] = " O";
                    break;

                    case "Right":
                    playerCol--;
                    if (playerCol < 0){
                        playerCol = 9;
                    }
                    world[playerRow][playerCol] = " O";
                    break;

                    case "Up":
                    playerRow++;
                    if (playerRow > 9){
                        playerRow = 0;
                    }
                    world[playerRow][playerCol] = " O";
                    break;

                    case "Down":
                    playerRow--;
                    if (playerRow < 0){
                        playerRow = 9;
                    }
                    world[playerRow][playerCol] = " O";
                    break;
                }

                spawnRope();
                return false;
            } else{
                return true;
            }

        }

        if (world[row][col].trim().equals("%O")){
            return true;
        }

        if (world[row][col].trim().equals("->O")){
            return false;
        }
        
        return false;
    }

    public void movePlayer(String direction){
        world[playerRow][playerCol] = " ";

        if (direction == "Up") {
            playerRow--;
            previousMove = "Up";
        }
        if (direction == "Down") {
            playerRow++;
            previousMove = "Down";
        }
        if (direction == "Left") {
            playerCol--;
            previousMove = "Left";
        }
        if (direction == "Right") {
            playerCol++;
            previousMove = "Right";
        }

        if (playerRow < 0){
            playerRow = 9;
        }
        if (playerRow > 9){
            playerRow = 0;
        }
        if (playerCol < 0){
            playerCol = 9;
        }
        if (playerCol > 9){
            playerCol = 0;
        }

        world[playerRow][playerCol] += "O";
    }

    public int checkAcquiredItem(int row, int col){
        //checks if an item is picks up and return item type
        if (world[row][col].trim().equals("--O")) {
            rope = true;
            clearCharacter("--");
            return 1;   
            //1 is rope
        } else if (world[row][col].trim().equals("->O")) {
            arrow = true;
            clearCharacter("->");
            return 2;
            //2 is arrow 
        } else {
            return 0;
            //0 is nothing 
        }
        
    }

    public void fireArrow(int direction, int row, int col) {
        //1 is left 
        if (direction == 1 & arrow == true) {
            if (world[row][col-1].trim().equals("%")) {
                dragonKilled = true;
            }  
        //2 is right 
        } else if (direction == 2 & arrow == true) {
            if (world[row][col+1].trim().equals("%")) {
               dragonKilled = true;
            } 
        // 3 is up 
        } else if (direction == 3 & arrow == true) {
            if (world[row-1][col].trim().equals("%")) {
                dragonKilled = true;
            } 
        //4 is down 
        } else if (direction == 4 & arrow == true) {
            if (world[row+1][col].trim().equals("%")) {
                dragonKilled = true;
            } 
        }
    }

    public void startWorld(){
        boolean dragonSpawn;
        boolean arrowSpawn;
        boolean playerSpawn;
        //Spawns player at (0,0)
        world[0][0] = "O";

        int randRow;
        int randColumn;
        Random rand = new Random();
        //Spaws pits
        do {
            for (int i = 0; i < 10; i++) {
                randRow = rand.nextInt(10);
                randColumn = rand.nextInt(10);

                if (world[randRow][randColumn] == " "){
                    world[randRow][randColumn] += "X"; 
                } else{
                    i--;
                }
                
                
            }

            if ((world[9][0] == "X") & (world[0][9] == "X") & (world[1][0] == "X") & (world[0][1] == "X")) {
                playerSpawn = false;
                clearCharacter("X");
            } else {
                playerSpawn = true; 
            }

        } while(playerSpawn == false);
       
    
        //Spawns arrow at random square 
        spawnArrow();
       
        //Spawns dragon at random square
        do {
            randRow = rand.nextInt(10);
            randColumn = rand.nextInt(10);
            if (checkSurroundings(randRow, randColumn) == false && (world[randRow][randColumn] == " ")){
                world[randRow][randColumn] = "%"; 
                dragonSpawn = true;
            } else {
                dragonSpawn = false;
                clearCharacter("%");
            }
        } while (dragonSpawn == false);

        
    } 

    

}