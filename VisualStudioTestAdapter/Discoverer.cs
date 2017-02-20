using Microsoft.VisualStudio.TestPlatform.ObjectModel.Adapter;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestPlatform.ObjectModel.Logging;
using Microsoft.VisualStudio.TestPlatform.ObjectModel;
using System.IO;
using System.Text.RegularExpressions;

namespace VisualStudioTestAdapter
{
	[DefaultExecutorUri( Executor.ExecutorUriString )]
	[FileExtension( ".py" )]
	[FileExtension( ".pyw" )]
	public class Discoverer : ITestDiscoverer
	{
		private static readonly Regex TestDecorator = new Regex( "^@Test(?:Case)?(?:\\s.*)?$" );
		private static readonly Regex FunctionExtractor = new Regex( "^def ([a-zA-Z_][a-zA-Z_0-9]+)\\(" );

		public void DiscoverTests( IEnumerable<string> sources, IDiscoveryContext discoveryContext, IMessageLogger logger, ITestCaseDiscoverySink discoverySink )
		{
			File.WriteAllText( "D:\\it works.txt", "it works!!!" );
			logger.SendMessage( TestMessageLevel.Informational, "lol" );
			throw new Exception( ".!." );

			foreach( var file in sources )
			{
				var lines = File.ReadAllLines( file );
				for( int i = 0; i < lines.Length; ++i )
				{
					var m = TestDecorator.Match( lines[ i ] );
					if( m.Success)
					{
						if( i == lines.Length - 1 )
						{
							logger.SendMessage( TestMessageLevel.Error, "Test decorator on the last line of the file" );
							continue;
						}

						++i;

						m = FunctionExtractor.Match( lines[ i ] );
						if( !m.Success || m.Groups.Count != 2 )
						{
							logger.SendMessage( TestMessageLevel.Error, "Wrong test function definition" );
							continue;
						}

						var test = new TestCase( m.Groups[ 1 ].Value, Executor.ExecutorUri, file )
						{
							CodeFilePath = file,
							DisplayName = m.Groups[ 1 ].Value,
							//Id = ,
							LineNumber = i,
						};

						discoverySink.SendTestCase( test );
					}
				}
			}
		}
	}
}
