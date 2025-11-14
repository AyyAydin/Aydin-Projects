import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class DDGUI implements ActionListener{

    JFrame frame;
    JPanel container, panel1, panel2, grid;
    JButton up, down, left, right, start, fireUp, fireDown, fireLeft, fireRight;
    JButton[][] world;
    JLabel label;
    JLabel notif;
    DDWorld DDWorld = new DDWorld();

    public DDGUI(){
        frame = new JFrame("Game");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800,800);

        JPanel container = new JPanel();
		container.setLayout(new BoxLayout(container, BoxLayout.Y_AXIS));

        panel1 = new JPanel();
        panel1.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        panel1.setBackground(Color.lightGray);

        grid = new JPanel();
        grid.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        grid.setBackground(Color.lightGray);
        grid.setLayout(new GridLayout(0, 10, 10, 5));

        panel2 = new JPanel();
        panel2.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        panel2.setBackground(Color.lightGray);
        panel2.setLayout(new GridLayout(0, 3, 10, 5));

        start = new JButton("Start");
        start.setActionCommand("Start");
        start.addActionListener(this);
        panel1.add(start);
        up = new JButton("Up");
        up.setActionCommand("Up");
        up.addActionListener(this);
        panel1.add(up);
        down = new JButton("Down");
        down.setActionCommand("Down");
        down.addActionListener(this);
        panel1.add(down);
        left = new JButton("Left");
        left.setActionCommand("Left");
        left.addActionListener(this);
        panel1.add(left);
        right = new JButton("Right");
        right.setActionCommand("Right");
        right.addActionListener(this);
        panel1.add(right);
        fireUp = new JButton("Fire Up");
        fireUp.setActionCommand("fireUp");
        fireUp.addActionListener(this);
        panel1.add(fireUp);
        fireDown = new JButton("Fire Down");
        fireDown.setActionCommand("fireDown");
        fireDown.addActionListener(this);
        panel1.add(fireDown);
        fireLeft = new JButton("Fire Left");
        fireLeft.setActionCommand("fireLeft");
        fireLeft.addActionListener(this);
        panel1.add(fireLeft);
        fireRight = new JButton("Fire Right");
        fireRight.setActionCommand("fireRight");
        fireRight.addActionListener(this);
        panel1.add(fireRight);

        world = new JButton[10][10];
        for (int i = 0; i < 10; i++){
            for (int j = 0; j < 10; j++){
                world[i][j] = new JButton(" ");
                world[i][j].setPreferredSize(new Dimension(60, 30));
                grid.add(world[i][j]);
            }
        }

        label = new JLabel("Press Start To Begin");
        label.setBorder(BorderFactory.createEmptyBorder(20, 0, 0, 0));
        panel2.add(label);

        notif = new JLabel("Notification: ");
        notif.setSize(notif.getPreferredSize());
        notif.setBorder(BorderFactory.createEmptyBorder(20, 0, 0, 0));
        panel2.add(notif);

        container.add(panel1);
		container.add(grid);
        container.add(panel2);

        frame.setContentPane(container);
        //frame.pack();
        frame.setVisible(true);
    }

    public void Transfer(){
        for (int i = 0; i < 10; i++){
            for (int j = 0; j < 10; j++){
                world[i][j].setText(DDWorld.world[i][j]);
            }
        }
    }

    public void Restart(){
        for (int i = 0; i < 10; i++){
            for (int j = 0; j < 10; j++){
                world[i][j].setText(" ");
                DDWorld.world[i][j] = " ";
            }
        }
        DDWorld.playerCol = 0;
        DDWorld.playerRow = 0;
        DDWorld.rope = true;
        DDWorld.arrow = false;
        DDWorld.dragonKilled = false;
        start.setText("Start");
        start.setActionCommand("Start");
    }

    public void moveChecks(){
        if (DDWorld.checkDead(DDWorld.playerRow, DDWorld.playerCol) == true){
            Restart();
            label.setText("Game over");
        } else if (DDWorld.rope == false){
            label.setText("Used rope");
            Transfer();
        } 
        if (DDWorld.checkAcquiredItem(DDWorld.playerRow, DDWorld.playerCol) == 1 ) {
            label.setText("Rope picked up");
        } else if (DDWorld.checkAcquiredItem(DDWorld.playerRow, DDWorld.playerCol) == 2 ) {
            label.setText("Arrow picked up");
        }

        notif.setText(DDWorld.notification(DDWorld.playerRow, DDWorld.playerCol));


    }

    public void fireArrow(){
        if (DDWorld.dragonKilled == true) {
            label.setText("Dragon killed!");
            Restart();
        } else if (DDWorld.arrow == false){
            label.setText("You do not have an arrow");
        } else {
            label.setText("Arrow missed");
            DDWorld.spawnArrow();
            Transfer();
        }   
    }

    public void actionPerformed(ActionEvent event) {
        String eventName = event.getActionCommand();
        
        if (eventName == "Start") {
            DDWorld.startWorld();
            Transfer();
            moveChecks();
            start.setText("Restart");
            start.setActionCommand("Restart");
            label.setText("Use buttons to move around and kill the dragon");
            //notif.setText("Notification");
        }  

        if (eventName == "Restart"){
            Restart();
        }

        if (eventName == "Up") { 
            DDWorld.movePlayer("Up");
            Transfer();
            moveChecks();
       }
        if (eventName == "Down") { 
            DDWorld.movePlayer("Down");
            Transfer();
            moveChecks();
       }
        if (eventName == "Right") {
             DDWorld.movePlayer("Right");
             Transfer();
             moveChecks();
        }
        if (eventName == "Left") {
            DDWorld.movePlayer("Left");
            Transfer();
            moveChecks();
        }

        if (eventName == "fireUp") {
            DDWorld.fireArrow(3, DDWorld.playerRow, DDWorld.playerCol);
            fireArrow();
        }
        if (eventName == "fireDown") {
            DDWorld.fireArrow(4, DDWorld.playerRow, DDWorld.playerCol);
            fireArrow();
        }
        if (eventName == "fireLeft") {
            DDWorld.fireArrow(1, DDWorld.playerRow, DDWorld.playerCol);
            fireArrow();
        }
        if (eventName == "fireRight") {
            DDWorld.fireArrow(2, DDWorld.playerRow, DDWorld.playerCol);
            fireArrow();
        }
    }

    /**
    * Create and show the GUI.
    */
    private static void runGUI() {
        JFrame.setDefaultLookAndFeelDecorated(true);
         DDGUI game = new DDGUI();
    }

    public static void main(String[] args) {
        /* Methods that create and show a GUI should be
        run from an event-dispatching thread */

        javax.swing.SwingUtilities.invokeLater(new Runnable() {
          public void run() {
           runGUI();
            }
         });
    }

}