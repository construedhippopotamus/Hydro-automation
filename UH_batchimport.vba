'Last updated July 2017
'configured for orange county AES - may need to change for other counties
'IMPORTS Q, v, and t from all .res unit hydrograph files in a folder to excel; one UH per tab. Currently only imports the first UH in the .res file.
'Need to change folder path. Will produce error if your AES file name has restricted character such as ":"

Sub rescheck()

Dim text As String
Dim title1 As String
Dim testcompare As String
Dim test2compare As String
Dim i As Integer
Dim j As Integer
Dim Folder As Object, File As Object, objFSO As Object
Dim rng1 As Range

Application.ScreenUpdating = False

Set objFSO = CreateObject("Scripting.FileSystemObject")
'Change folder path
Set Folder = objFSO.GetFolder("H:\pdata\134519\Calcs\Strmwater\PA-3 & PA-4\Hydrology\Local\Ultimate\Unit Hydrograph\Complex\Expected Value\100-yr")


i = 1
Close #1

For Each File In Folder.Files
            
        If Right(File.Name, 4) = ".RES" Then
            
            Open File For Input As #1
            
            test2compare = "-----------"   'end condition:
            j = 2
                   
            'DELETE contents of sheet
            'Sheets(i).Range("A1:F3000").ClearContents
            
            Do Until EOF(1)
                Line Input #1, text  'Line input reads a single line from an open sequential file and assigns it to a String variable.
                testcompare = Left(text, 11)
                   
                If testcompare = "  TIME(HRS)" Then
                
                    Do Until Left(testcompare, 11) = test2compare   'stop copying
                        Line Input #1, text
                        'Cells(j, 1).Value = text
                        Sheets(i).Cells(j, 2).Value = Left(text, 9)
                        Sheets(i).Cells(j, 3).Value = Right(Left(text, 25), 15)
                        Sheets(i).Cells(j, 4).Value = Right(Left(text, 31), 10)
                      
                        j = j + 1
                        testcompare = Left(text, 11)
                  
                    Loop
                    
                ElseIf testcompare = "   FILE NAM" Then
                       
                    title1 = text
                                        
                 End If
            Loop
            
            Sheets(i).Cells(1, 1) = title1
            'cannot use whole title for sheet name because ":" is restricted
            Sheets(i).Name = Right(Trim(title1), 11)
            
            'delete last line of dashes
            Set rng1 = Sheets(i).UsedRange.Find("*", Sheets(i).[a1], xlValues, , xlByRows, xlPrevious)
            If Not rng1 Is Nothing Then rng1.EntireRow.Delete
            
            Close #1
            
            Sheets(i).Cells(2, 2) = "time, hrs"
            Sheets(i).Cells(2, 3) = "vol, AF"
            Sheets(i).Cells(2, 4) = "Q, cfs"

            i = i + 1
            
            Sheets.Add After:=ActiveSheet
            
        End If

Next File


End Sub

