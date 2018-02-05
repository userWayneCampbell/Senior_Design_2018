using System;
using System.Diagnostics;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using PythonLib;


namespace MainApp_2
{
    public partial class Main : Form
    {
        public Main()
        {
            InitializeComponent();
            PythonLib.Init.IntFilePathDate();
        }

        private void btn_Choose_Click(object sender, EventArgs e)
        {
            Form ChooseForm = new Segment_Chooser.Main(PythonLib.Init.filepathDate);
            ChooseForm.Show();
        }

        /// <summary>
        /// Runs Python to create directory and save initial picture
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btn_testRunningPython_Click(object sender, EventArgs e)
        {
            Form test = new PythonService(PythonLib.Init.filepathDate);
            test.Show();
        }

        
    }
}
