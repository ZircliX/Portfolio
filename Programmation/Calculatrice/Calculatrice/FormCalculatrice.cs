using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Media;

namespace Calculatrice
{
    public partial class FormCalculatrice : Form
    {
        private Calcul calculate;
        private Memory memory;

        public FormCalculatrice()
        {
            InitializeComponent();

            calculate = new Calcul();
            memory = new Memory();

            //textBoxEnterResult.Text = "0,";

            this.Focus();
        }

        //
        // Set displayed TextBox
        // while user click on button's number
        //
        private void buttonNumber_Click(object sender, EventArgs e)
        {
            if ( calculate.CalculState == CalculStateEnum.BeginAquireOperand2 )
            {
                // Clear Enter
                textBoxEnterResult.Text = string.Empty;
                calculate.CalculState = CalculStateEnum.AquireOperand2;
            }

            if ( memory.MemorySate == MemoryStateEnum.Saved )
            {
                textBoxEnterResult.Text = string.Empty;
                memory.MemorySate = MemoryStateEnum.Full;
            }

            string sNumber = (sender as Button).Text;
            textBoxEnterResult.Text += sNumber;
        }

        //
        // Verify first operand is NOT set then set
        // Get the oprand
        // Clear the TextBox
        //
        private void buttonOperand_Click(object sender, EventArgs e)
        {
            string sOperand = (sender as Button).Text;
            calculate.Operation = sOperand;

            if ( calculate.CalculState == CalculStateEnum.AquireOperand1 )
            {
                double result;
                try
                {
                    result = Double.Parse(textBoxEnterResult.Text);
                    calculate.Operand1 = result;
                    calculate.CalculState = CalculStateEnum.BeginAquireOperand2;
                }
                catch (Exception)
                {
                }
            }
        }

        //
        // Verify first operand is set
        // then display the result of the calculation
        //
        private void buttonEqual_Click(object sender, EventArgs e)
        {
            if ( calculate.CalculState == CalculStateEnum.AquireOperand2 )
            {
                double result;
                try
                {
                    result = Double.Parse(textBoxEnterResult.Text);
                    calculate.Openrad2 = result;
                    calculate.CalculState = CalculStateEnum.Calculation;
                }
                catch (Exception)
                {
                }
            }

            if ( calculate.CalculState == CalculStateEnum.BeginAquireOperand2 )
            {
                calculate.CalculState = CalculStateEnum.Calculation;
            }

            if ( calculate.CalculState == CalculStateEnum.Calculation )
            {
                double result = calculate.Calculate();
                textBoxEnterResult.Text = result.ToString();

                // Result become the first operand
                calculate.Operand1 = result;

                // Effacer avant d'aquérir opérande2
                calculate.CalculState = CalculStateEnum.BeginAquireOperand2;
            }
        }

        //
        // Suppress last caracter to the TextBox
        // 
        private void buttonGoBack_Click(object sender, EventArgs e)
        {
            if ( textBoxEnterResult.Text.Length > 0 )
            {
                textBoxEnterResult.Text = textBoxEnterResult.Text.Substring(0, textBoxEnterResult.Text.Length - 1);
            }
        }

        // Manage +/- touch
        private void buttonPlusMinus_Click(object sender, EventArgs e)
        {
            if ( textBoxEnterResult.Text.Length > 0 )
            {
                string signe = textBoxEnterResult.Text[0].ToString();

                if (string.Compare(signe, "-") == 0)
                {
                    textBoxEnterResult.Text = textBoxEnterResult.Text.Substring(1, textBoxEnterResult.Text.Length - 1);
                }
                else
                {
                    textBoxEnterResult.Text = "-" + textBoxEnterResult.Text;
                }
            }

        }

        private void buttonComma_Click(object sender, EventArgs e)
        {
            if (textBoxEnterResult.Text.Length > 0)
            {
                if (textBoxEnterResult.Text.Contains( "," ) == false)
                {
                    textBoxEnterResult.Text = textBoxEnterResult.Text + ",";
                }
                else
                {
                    SystemSounds.Beep.Play();
                }
            }
            else
            {
                textBoxEnterResult.Text = textBoxEnterResult.Text + "0,";
            }
        }

#region Clear Buttons

        private void buttonClearDisplay_Click(object sender, EventArgs e)
        {
            textBoxEnterResult.Text = "";
        }

        private void buttonClearCalculation_Click(object sender, EventArgs e)
        {
            calculate = new Calcul();
            textBoxEnterResult.Text = "";
        }

#endregion

#region Memory Management

        private void buttonMemorySave_Click(object sender, EventArgs e)
        {
            if ( textBoxEnterResult.Text.Length > 0 )
            {
                try
                {
                    memory.Memory1 = Double.Parse( textBoxEnterResult.Text );
                    memory.MemorySate = MemoryStateEnum.Saved;
                    labelMemory.Text = "M";
                }
                catch (Exception)
                {
                }
            }
        }

        private void buttonMemoryAdd_Click( object sender, EventArgs e )
        {
            try
            {
                memory.Memory1 += Double.Parse( textBoxEnterResult.Text );
                memory.MemorySate = MemoryStateEnum.Saved;
                labelMemory.Text = "M";
            }
            catch (Exception)
            {
            }
        }

        private void buttonMemoryRead_Click( object sender, EventArgs e )
        {
            textBoxEnterResult.Text = memory.Memory1.ToString();
            memory.MemorySate = MemoryStateEnum.Saved;

            // Memory est affiché, demander l'aquisition de l'operande2
            calculate.CalculState = CalculStateEnum.AquireOperand2;
        }

        private void buttonMemoryClear_Click( object sender, EventArgs e )
        {
            labelMemory.Text = string.Empty;
            memory = new Memory();
        }

        #endregion

        private void FormCalculatrice_KeyPress( object sender, KeyPressEventArgs e )
        {
            Button button1 = new Button();
            button1.Text = e.KeyChar.ToString();

            //
            // Nombre de 0 à 9
            //
            if (e.KeyChar >= 48 && e.KeyChar <= 57)
            {
                // Simuler un click sur un bouton chiffre
                buttonNumber_Click( button1, e );
            }

            //
            // Traitement operands
            //
            string operand = "/*+-";

            if (operand.Contains( e.KeyChar ))
            {
                buttonOperand_Click( button1, e );
            }

            //
            // Calculation
            //
            if (e.KeyChar == '=' )
            {
                buttonEqual_Click( button1, e );
            }

            if (e.KeyChar == '\r')
            {
                button1.Text = "=";
                buttonEqual_Click( button1, e );
            }

            if (e.KeyChar == '\b')
            {
                buttonGoBack_Click( button1, e );
            }
        }
    }
}
