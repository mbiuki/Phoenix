//
// This program extracts data from the txt dump of an APM Mission Planner log file. The output
// data is stored as a comma separated value (CSV) file that can be opened in Excel. Note that it can't
// open the tlog file directly. You must use the Mission Planner to convert it to txt format.
//
// From the APM Mission Planner Flight Data page select "Telemetry Logs", then "Tlog > Kml or Graph", then "Convert to Text".
// Select the tlog file you are interested in, and the Mission Planner will create a txt file in its log folder.
// 
// Open the txt file in this program and it will parse the file and list the available parameters. Double click on the parameters you
// are interested in and they will be selected. "Save As" and provide an output file name. That's it.
//
//


using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;

namespace TLogDataExtractor
{


    public partial class MainForm : Form
    {
        string configurationFileName;
        string inputFileName;
        string outputFileName;

        StreamReader inputFile;
        StreamReader configurationFileIn;
        StreamWriter configurationFileOut;
        StreamWriter outputFile;

        class ParameterDefinition
        {
            public string packetName;
            public string parameterName;
            public double value;

            public ParameterDefinition(string pktName, string paramName, double val)
            {
                this.packetName = pktName;
                this.parameterName = paramName;
                this.value = val;
            }
        }


        List<ParameterDefinition> parameterList = new List<ParameterDefinition>();
        List<ParameterDefinition> inputFileParameterList = new List<ParameterDefinition>();

        
        public MainForm()
        {
            InitializeComponent();
        }

        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            String inputLine;

            string packetType = "";
            string[] inputLineSplit;
            bool foundPacketType;
            bool addNodes;
            bool newPacketType = false;
            bool param_type=true;


            OpenFileDialog dlg = new OpenFileDialog();
            dlg.Filter = "Text Documents (*.txt)|*.txt|All Files|*.*";
            dlg.ShowDialog();
            inputFileName = dlg.FileName;
            TreeNode tnPacketNode = null;

            inputFile = new StreamReader(inputFileName);

            inputLine = inputFile.ReadLine();

            while (inputLine != null)
            {
                inputLineSplit = inputLine.Split(' ');

                foundPacketType = false;
                addNodes = false;

                param_type = false;

                foreach (string field in inputLineSplit)
                {
                    if (!foundPacketType)
                    {
                        if (field.Contains("mavlink_"))
                        {
                            foundPacketType = true;
                            packetType = field;

                            newPacketType = true;

                            foreach (TreeNode tnPacket in fileParametersTree.Nodes)
                            {
                                if (String.Compare(tnPacket.Text, packetType, true) == 0)
                                    newPacketType = false;
                            }

                        }

                    }

                    if (newPacketType == true)
                    {
                        tnPacketNode = fileParametersTree.Nodes.Add(packetType);
                        newPacketType = false;
                        addNodes = true;
                    }

                    if (addNodes && (field.Length>0))
                    {
                        if (param_type)
                        {
                            tnPacketNode.Nodes.Add(field);
                        }

                        param_type = !param_type;

                    }
                }

                inputLine = inputFile.ReadLine();
            }

            inputFile.Close();
        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        //
        // SaveAs parses the input file extracts the desires parameters, amd saves them in a CSV (comma separated values) format text file
        //
        private void saveAsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            String inputLine;
            int parameterIndexInString;
            bool parameterInString;
            int parameterEnd;
            String parameterValue;
            string[] inputLineSplit;

            SaveFileDialog dlg = new SaveFileDialog();
            dlg.Filter = "Comma Separated Values Documents (*.csv)|*.csv|All Files|*.*";
            dlg.ShowDialog();
            outputFileName = dlg.FileName;

            outputFile = new StreamWriter(outputFileName);
            inputFile = new StreamReader(inputFileName);
            
            //
            // Output the header row
            //
            outputFile.Write("Date, Time");         // start with the Date and Time fields
                
            foreach (TreeNode tn in selectedParametersTree.Nodes)       // then each of the selected parameters
            {
                foreach (TreeNode tpn in tn.Nodes)
                {
                    outputFile.Write(", {0}.{1}", tn.Text, tpn.Text);   // format is PacketName.ParameterName
                }
            }
            outputFile.WriteLine();


            //
            // Parse each line in the input file
            //
            inputLine = inputFile.ReadLine();
            while (inputLine != null)
            {
                parameterInString = false;

                inputLineSplit = inputLine.Split(' ');

                // search in each line for the packet name of each of the selected parameters
                foreach (TreeNode tn in selectedParametersTree.Nodes)
                {
                    if (inputLine.Contains(tn.Text))
                    {
                        // if the packet name was found, search the line for each parameter 
                        foreach (TreeNode tpn in tn.Nodes)
                        {
                            parameterIndexInString = inputLine.IndexOf(tpn.Text);

                            if (parameterIndexInString != -1)
                            {
                                parameterIndexInString = parameterIndexInString + tpn.Text.Length + 1;   // Skip parameter name + 1 for the " " between the parameter name and the value
                                parameterEnd = inputLine.IndexOf(' ', parameterIndexInString);
                                parameterValue = inputLine.Substring(parameterIndexInString, parameterEnd - parameterIndexInString);
                                tpn.Tag = parameterValue;
                                parameterInString = true;
                            }
                        }
                    }
                }

                // 
                // If at least parameter was found, write them all to the output file.
                if (parameterInString)
                {
                    outputFile.Write("{0}, {1} ", inputLineSplit[0], inputLineSplit[1]);         // Date and time fields

                    foreach (TreeNode tn in selectedParametersTree.Nodes)
                    {
                        foreach (TreeNode tpn in tn.Nodes)
                        {
                            outputFile.Write(", {0}", tpn.Tag);
                        }
                    }
                    outputFile.WriteLine("");
                }

                inputLine = inputFile.ReadLine();
            }

            outputFile.Close();
            inputFile.Close();
        }

        //
        // Load a file containing a list of parameters
        //
        private void loadParametersToolStripMenuItem_Click(object sender, EventArgs e)
        {
            string strLine;
            char[] separators = new char[] { ' ', ',' };
            string[] parts;
            bool newPacketType;
            bool newParamType;
            TreeNode tnPacketNode=null;
            TreeNode tnParamNode=null;

            OpenFileDialog dlg = new OpenFileDialog();
            dlg.Filter = "Text Documents (*.txt)|*.txt|All Files|*.*";
            dlg.ShowDialog();
            configurationFileName = dlg.FileName;

            configurationFileIn = new StreamReader(configurationFileName);

            strLine = configurationFileIn.ReadLine();

            while (strLine != null)
            {
                parts = strLine.Split(separators, StringSplitOptions.RemoveEmptyEntries);

                newPacketType = true;

                foreach (TreeNode tn in selectedParametersTree.Nodes)
                {
                    if (String.Compare(tn.Text, Convert.ToString(parts[0]), true) == 0)
                    {
                        tnPacketNode = tn;
                        newPacketType = false;
                    }
                }

                if (newPacketType == true)
                    tnPacketNode = selectedParametersTree.Nodes.Add(Convert.ToString(parts[0]));

                newParamType = true;

                foreach (TreeNode tpn in tnPacketNode.Nodes)
                {
                    if (String.Compare(tpn.Text, Convert.ToString(parts[1]), true) == 0)
                    {
                        tnParamNode = tpn;
                        newParamType = false;
                    }
                }

                if (newParamType == true)
                {
                    tnParamNode = tnPacketNode.Nodes.Add(Convert.ToString(parts[1]));
                    tnParamNode.Tag = 0;
                }

                strLine = configurationFileIn.ReadLine();
            }

            configurationFileIn.Close();
        }

        // 
        // Save the list of selected parameters
        //
        private void saveParameterListToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SaveFileDialog dlg = new SaveFileDialog();
            dlg.Filter = "Text Documents (*.txt)|*.txt|All Files|*.*";
            dlg.ShowDialog();

            configurationFileOut = new StreamWriter(dlg.FileName);

            foreach (TreeNode tn in selectedParametersTree.Nodes)
            {
                foreach (TreeNode tpn in tn.Nodes)
                {
                    configurationFileOut.WriteLine("{0} {1}", tn.Text, tpn.Text);
                }
            }

            configurationFileOut.Close();
        }

        //
        // Responds to the user double-clicking in the input file parameter list by adding the parameter to the output file list
        //
        private void fileParametersTree_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            TreeNode tnPacketNode=null;
            TreeNode tnParamNode;
            bool newPacketType;
            bool newParamType;

            TreeNode tnPacket = fileParametersTree.SelectedNode.Parent;

            if(tnPacket!=null)
            {

                // Check for repeat
                newPacketType = true;

                foreach (TreeNode tn in selectedParametersTree.Nodes)
                {
                    if (String.Compare(tn.Text, tnPacket.Text, true) == 0)
                    {
                        tnPacketNode = tn;
                        newPacketType = false;
                    }
                }

                if (newPacketType == true)
                     tnPacketNode = selectedParametersTree.Nodes.Add(tnPacket.Text);

                newParamType = true;

                foreach (TreeNode tpn in tnPacketNode.Nodes)
                {
                    if (String.Compare(tpn.Text, fileParametersTree.SelectedNode.Text, true) == 0)
                    {
                        tnParamNode = tpn;
                        newParamType = false;
                    }
                }

                if (newParamType == true)
                {
                    tnParamNode = tnPacketNode.Nodes.Add(fileParametersTree.SelectedNode.Text);
                    tnParamNode.Tag = 0.0;
                }
            }
        }

        //
        // Responds to the user double-clicking in the output file parameter list by removing that parameter from the list
        //
        private void selectedParametersTree_NodeMouseDoubleClick(object sender, TreeNodeMouseClickEventArgs e)
        {

            TreeNode tnPacket = selectedParametersTree.SelectedNode.Parent;

            if (tnPacket != null)
            {
                selectedParametersTree.SelectedNode.Remove();
                if (tnPacket.Nodes.Count == 0)
                    tnPacket.Remove();
            }
 
        }

        private void fileParametersTree_AfterSelect(object sender, TreeViewEventArgs e)
        {

        }
    }
}
